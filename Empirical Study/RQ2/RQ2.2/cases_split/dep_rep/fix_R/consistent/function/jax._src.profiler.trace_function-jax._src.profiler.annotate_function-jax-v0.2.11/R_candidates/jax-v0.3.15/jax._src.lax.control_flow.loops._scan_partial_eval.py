def _scan_partial_eval(trace, *tracers, reverse, length, num_consts, num_carry,
                       jaxpr, linear, unroll):
  num_ys = len(jaxpr.out_avals) - num_carry
  unknowns = [not t.pval.is_known() for t in tracers]
  const_uk, init_uk, xs_uk = split_list(unknowns, [num_consts, num_carry])

  # Fixpoint computation of which carry elements are unknown. Each iteration
  # promotes at least one carry to unknown. We need at most len(carry)
  # iterations, but we need one last iteration to prepare the jaxpr based on the
  # final carry_uk.
  carry_uk = init_uk
  for _ in range(1 + len(carry_uk)):
    unknowns = const_uk + carry_uk + xs_uk
    jaxpr_known, jaxpr_unknown, out_uk, res_avals = pe.partial_eval_jaxpr_nounits(
        jaxpr, unknowns, instantiate=carry_uk + [False] * num_ys)
    carry_uk_out, ys_uk = split_list(out_uk, [num_carry])
    if carry_uk_out == carry_uk:
      break
    else:
      carry_uk = _map(operator.or_, carry_uk, carry_uk_out)
  else:
    assert False, "Fixpoint not reached"
  num_res = len(res_avals)
  del res_avals, carry_uk_out

  # Instantiate those inputs which must be treated as unknown from the fixpoint.
  tracers = [trace.instantiate_const(t) if uk else t
             for t, uk in zip(tracers, unknowns)]

  # The residual inputs and outputs of the jaxprs produced haven't yet been
  # adapted to the scan calling convention; in particular, jaxpr_known has its
  # residual outputs all at the end, meaning they're extensive outputs (which is
  # fully general but may be wasteful for residuals which are loop-invariant)
  # while jaxpr_unknown has its corresponding residual inputs at the front (just
  # as a convention with partial_eval_jaxpr_nounits), making them constant
  # inputs. To make them consistent, we move the residual inputs on
  # jaxpr_unknown to the end, even though we may move some back in the sequel.
  jaxpr_unknown = pe.move_binders_to_back(
      jaxpr_unknown, [True] * num_res + [False] * sum(unknowns))

  # At this point, all residuals are treated as extensive outputs of jaxpr_known
  # (and extensive inputs to jaxpr_unknown). But residuals that are loop-
  # invariant can be hoisted out of the scan, rather than letting them get
  # broadcast (as in e.g. scanning multiplication by a constant matrix; we don't
  # want to broadcast the matrix!). So, outside the loop we perform a partial
  # evaluation with known 'const' inputs (but all other inputs unknown).
  const_pvals = [pe.PartialVal.known(t.pval.get_known())
                 for t in tracers[:num_consts] if t.pval.is_known()]
  other_pvals = [pe.PartialVal.unknown(aval)
                 for aval in jaxpr_known.in_avals[len(const_pvals):]]
  with source_info_util.reset_name_stack():
    jaxpr_known_, invar_pvals_out, jaxpr_known_consts = pe.trace_to_jaxpr_nounits(
        lu.wrap_init(core.jaxpr_as_fun(jaxpr_known)), const_pvals + other_pvals,
        instantiate=[True] * (len(out_uk) - sum(out_uk)) + [False] * num_res)
  jaxpr_known = pe.ClosedJaxpr(pe.convert_constvars_jaxpr(jaxpr_known_), ())
  # The above trace_to_jaxpr_nounits call computed loop-invariant residuals
  # (known values in invar_pvals_out) and also computed loop-invariant values
  # needed by the new jaxpr_known (in jaxpr_known_consts, which replace the
  # previous consts). We need to collect the computed inteisive residuals, and
  # move corresponding intensive residual binders in jaxpr_unknown to the front.
  res_pvals = invar_pvals_out[len(invar_pvals_out) - num_res:]
  intensive_res = [pval.get_known() for pval in res_pvals if pval.is_known()]
  jaxpr_unknown = pe.move_binders_to_front(
      jaxpr_unknown,
      [False] * sum(unknowns) + [pval.is_known() for pval in res_pvals])
  del const_pvals, other_pvals, invar_pvals_out, jaxpr_known_, res_pvals
  # We use `jaxpr_known_consts` when we call scan_p.bind with jaxpr_known, and
  # we use `intensive_res` when we build the jaxpr eqn with jaxpr_unknown.

  # As another optimization, for any extensive inputs that are just forwarded to
  # extensive outputs, to avoid a copy (which would be looping over
  # dynamic-update-slice) we'd rather forward the input tracer/value. That means
  # pruning some outputs from jaxpr_known here, and updating `out_flat` below.
  fwds_known = pe._jaxpr_forwarding(jaxpr_known.jaxpr)
  # Prune fwds_known to include only extensive input to extensive output.
  fwds_known = [in_idx if out_idx >= num_carry - sum(carry_uk) and
                in_idx is not None and
                in_idx >= len(jaxpr_known_consts) + num_carry - sum(carry_uk)
                else None for out_idx, in_idx in enumerate(fwds_known)]
  # Drop any extensive output we can instead get by forwarding an input.
  # TODO(mattjj): use pe.dce_jaxpr here, though need a fixpoint
  jaxpr_known_, () = jaxpr_known.jaxpr, jaxpr_known.consts
  jaxpr_known_.outvars = [x for x, i in zip(jaxpr_known_.outvars, fwds_known)
                          if i is None]
  jaxpr_known = core.ClosedJaxpr(jaxpr_known_, ())
  del jaxpr_known_
  # We use `fwds_known` below when forming the output of scanning jaxpr_known.

  # Run the known part of the scan (if it has any outputs or effects).
  known_inputs = (list(jaxpr_known_consts) +
                  [t.pval.get_known() for t in tracers[num_consts:]
                   if t.pval.is_known()])
  if not jaxpr_known.out_avals and not jaxpr_known.effects:
    out_known = []
  else:
    linear_known = [False] * len(known_inputs)  # conservative!
    out_known = scan_p.bind(
        *known_inputs, reverse=reverse, length=length, jaxpr=jaxpr_known,
        num_consts=len(jaxpr_known_consts), num_carry=num_carry - sum(carry_uk),
        linear=tuple(linear_known), unroll=unroll)
    del linear_known
  # Complete the known output by filling in forwarded values using fwds_known.
  out_known_iter = iter(out_known)
  out_known = [next(out_known_iter) if f is None
               else _maybe_put(known_inputs[f]) for f in fwds_known]
  assert next(out_known_iter, None) is None
  del known_inputs, out_known_iter

  # Split known outputs from residuals.
  out_known, extensive_res = split_list(out_known, [len(out_uk) - sum(out_uk)])
  assert len(intensive_res) + len(extensive_res) == num_res

  # Create input tracers for jaxpr_unknown bind.
  unknown_inputs = [t for t in tracers if not t.pval.is_known()]
  intensive_res = _map(trace.new_instantiated_const, intensive_res)
  extensive_res = _map(trace.new_instantiated_const, extensive_res)
  # Create output tracers for jaxpr_unknown bind, adapting extensive shapes.
  carry_avals, y_avals = split_list(jaxpr_unknown.out_avals, [sum(carry_uk)])
  ys_avals = [core.unmapped_aval(length, core.no_axis_name, 0, y_aval)
              for y_aval in y_avals]
  out_tracers = [pe.JaxprTracer(trace, pe.PartialVal.unknown(a), None)
                 for a in itertools.chain(carry_avals, ys_avals)]
  del carry_avals, y_avals
  # Create equation.
  linear_unknown = tuple([False] * len(intensive_res) +
                         [l for l, uk in zip(linear, unknowns) if uk] +
                         [False] * len(extensive_res))
  name_stack = source_info_util.current_name_stack()[len(trace.name_stack):]
  source = source_info_util.current().replace(name_stack=name_stack)
  assert len(out_tracers) == len(jaxpr_unknown.out_avals)
  eqn = pe.new_eqn_recipe([*intensive_res, *unknown_inputs, *extensive_res],
                          out_tracers, scan_p,
                          dict(reverse=reverse, length=length, unroll=unroll,
                               jaxpr=jaxpr_unknown, linear=linear_unknown,
                               num_consts=len(intensive_res) + sum(const_uk),
                               num_carry=sum(carry_uk)),
                          jaxpr_unknown.effects, source)
  for t in out_tracers: t.recipe = eqn

  # Merge known and unknown outputs into final result.
  return util.merge_lists(out_uk, out_known, out_tracers)
