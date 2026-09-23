def _scan_partial_eval_custom(saveable, unks_in, inst_in, eqn):
  jaxpr = eqn.params['jaxpr']
  num_consts, num_carry = eqn.params['num_consts'], eqn.params['num_carry']
  num_ys = len(jaxpr.out_avals) - num_carry

  # Fixpoint (trivial on 'inst_in', since we might as well make all inputs
  # available as DCE can subsequently prune any unused ones)
  const_uk, carry_uk, xs_uk = split_list(unks_in, [num_consts, num_carry])
  for _ in range(1 + len(carry_uk)):
    unks_in = const_uk   + carry_uk   + xs_uk
    jaxpr_known_, jaxpr_staged_, unks_out, inst_out, num_res = \
        pe.partial_eval_jaxpr_custom(
            jaxpr.jaxpr, in_unknowns=unks_in, in_inst=True,
            ensure_out_unknowns=carry_uk + [False] * num_ys,
            ensure_out_inst=True, saveable=saveable)
    carry_uk_out, ys_uk = split_list(unks_out, [num_carry])
    if carry_uk_out == carry_uk:
      break
    else:
      carry_uk = _map(operator.or_, carry_uk, carry_uk_out)
  else:
    assert False, "Fixpoint not reached"
  jaxpr_known  = core.ClosedJaxpr(jaxpr_known_ , jaxpr.consts)
  jaxpr_staged = core.ClosedJaxpr(jaxpr_staged_, jaxpr.consts)

  # Move all residual binders to the back of jaxpr_staged so they're extensive.
  # TODO(mattjj): make jaxpr_staged only take instantiated inputs
  res_avals = jaxpr_staged.in_avals[:num_res]
  jaxpr_staged = pe.move_binders_to_back(
      jaxpr_staged, [True] * num_res + [False] * len(jaxpr.in_avals))

  # Instantiate all inputs (b/c jaxpr_staged takes all inputs, corresponding to
  # passing in_inst argument to partial_eval_jaxpr_custom above).
  new_inst = [x for x, inst in zip(eqn.invars, inst_in)
              if type(x) is core.Var and not inst]
  inst_in = [True] * len(inst_in)

  # As an optimization, hoist loop-invariant residuals out of the loop rather
  # than using extensive outputs for them. See _scan_partial_eval for comments.
  num_const_known = len(const_uk) - sum(const_uk)
  num_carry_known = len(carry_uk) - sum(carry_uk)
  num_xs_known    = len(   xs_uk) - sum(   xs_uk)
  jaxpr_known_hoist, jaxpr_known_loop, loop_dep, consts_known_lp_avals = \
      pe.partial_eval_jaxpr_nounits(
          jaxpr_known,
          [False] * num_const_known + [True] * (num_carry_known + num_xs_known),
          [True] * (len(unks_out) - sum(unks_out)) + [False] * num_res)
  # jaxpr_known_hoist produces intensive residuals followed by the constants for
  # jaxpr_known_loop. We adjust jaxpr_staged to accept intensive res as consts.
  _, loop_dep_res = split_list(loop_dep, [len(loop_dep) - num_res])
  jaxpr_staged = pe.move_binders_to_front(
      jaxpr_staged, [False] * sum(inst_in) + _map(operator.not_, loop_dep_res))
  num_intensive_res = len(loop_dep_res) - sum(loop_dep_res)
  del loop_dep, num_carry_known, num_xs_known, const_uk

  # Create residual variables.
  intensive_avals, ext_avals_mapped = partition_list(loop_dep_res, res_avals)
  ext_avals = [core.unmapped_aval(eqn.params['length'], core.no_axis_name, 0, a)
               for a in ext_avals_mapped]
  newvar = core.gensym()
  intensive_res = _map(newvar, intensive_avals)
  extensive_res = _map(newvar, ext_avals)

  # Create known eqn, which is a call_p combining evaluation of
  # jaxpr_known_hoist and a scan of jaxpr_known_loop.
  ins_known, _ = partition_list(unks_in, eqn.invars)
  out_binders_known, _ = partition_list(unks_out, eqn.outvars)
  # jaxpr_known_loop takes as input constants output as res by jaxpr_known_hoist
  # (corresponding to consts_known_lp_avals) followed by known carry and xs.
  linear_known_ = [l for l, uk in zip(eqn.params['linear'], unks_in) if not uk]
  _, linear_known_ = split_list(linear_known_, [num_const_known])
  linear_known = [False] * len(consts_known_lp_avals) + linear_known_
  params_known = dict(eqn.params, jaxpr=jaxpr_known_loop,
                      num_consts=len(consts_known_lp_avals),
                      num_carry=len(carry_uk)-sum(carry_uk),
                      linear=tuple(linear_known))

  @lu.wrap_init
  def known(*ins_known):
    consts_known_hoist, ins_known_lp = split_list(ins_known, [num_const_known])
    out_hoist = core.jaxpr_as_fun(jaxpr_known_hoist)(*consts_known_hoist)
    intensive_res, consts_known_lp = split_list(out_hoist, [num_intensive_res])
    out_loop = scan_p.bind(*consts_known_lp, *ins_known_lp, **params_known)
    return [*intensive_res, *out_loop]
  call_jaxpr_, _, call_jaxpr_consts = pe.trace_to_jaxpr_dynamic(
      known, [v.aval for v in ins_known])
  call_jaxpr = core.ClosedJaxpr(call_jaxpr_, call_jaxpr_consts)
  eqn_known = pe.new_jaxpr_eqn(
      ins_known, [*intensive_res, *out_binders_known, *extensive_res],
      core.closed_call_p, dict(call_jaxpr=call_jaxpr), call_jaxpr.effects,
      eqn.source_info)

  # Create the staged eqn.
  _, out_binders_staged = partition_list(inst_out, eqn.outvars)
  linear_staged = ([False] * len(intensive_res) + list(eqn.params['linear']) +
                   [False] * len(extensive_res))
  params_staged = dict(eqn.params, jaxpr=jaxpr_staged,
                       num_consts=len(intensive_res) + eqn.params['num_consts'],
                       linear=tuple(linear_staged))
  eqn_staged = pe.new_jaxpr_eqn([*intensive_res, *eqn.invars, *extensive_res],
                                out_binders_staged, eqn.primitive,
                                params_staged, jaxpr_staged.effects,
                                eqn.source_info)

  new_vars = [*new_inst, *intensive_res, *extensive_res]
  return eqn_known, eqn_staged, unks_out, inst_out, new_vars
