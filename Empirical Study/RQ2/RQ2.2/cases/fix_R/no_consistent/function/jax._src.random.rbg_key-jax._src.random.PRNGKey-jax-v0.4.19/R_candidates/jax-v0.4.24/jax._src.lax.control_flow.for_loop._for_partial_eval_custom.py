def _for_partial_eval_custom(saveable, in_unknowns, in_inst, eqn):
  jaxpr, nsteps, reverse, which_linear, unroll = split_dict(
      eqn.params, ["jaxpr", "nsteps", "reverse", "which_linear", "unroll"])
  num_inputs = len(eqn.invars)
  # We first need to run a fixpoint to determine which of the `Ref`s are unknown
  # after running the for loop. However, the jaxpr has no outputs. Instead, we
  # discharge the body and run the fixpoint with the discharged jaxpr. We can do
  # this because the outputs of the discharged jaxpr are one-to-one with the
  # inputs.
  discharged_jaxpr, discharged_consts = discharge_state(jaxpr, ())
  discharged_jaxpr = discharged_jaxpr.replace(
      invars=discharged_jaxpr.constvars + discharged_jaxpr.invars,
      constvars=[])
  in_unknowns, in_inst = list(in_unknowns), list(in_inst)
  out_unknowns, out_inst =  in_unknowns, in_inst
  for _ in range(num_inputs):
    jaxpr_in_unknowns = [False] * len(discharged_consts) + [False, *in_unknowns]
    _, _, out_unknowns, out_inst, _, = pe.partial_eval_jaxpr_custom(
        discharged_jaxpr, jaxpr_in_unknowns, True,
          ensure_out_unknowns=in_unknowns, ensure_out_inst=True,
          saveable=saveable)
    out_unknowns = list(out_unknowns)
    if out_unknowns == in_unknowns:
      break
    in_unknowns = map(operator.or_, in_unknowns, out_unknowns)
  else:
    if num_inputs > 0: raise Exception("Invalid fixpoint")
  del out_unknowns # Redundant since it's the same as `in_unknowns`
  new_inst = [x for x, inst in zip(eqn.invars, in_inst)
              if type(x) is core.Var and not inst]
  in_inst = [True] * len(eqn.invars)

  # We use `partial_eval_jaxpr_custom` here because it won't remove effectful
  # primitives like `get`/`set`.
  jaxpr_known_resout, jaxpr_staged_resin_, _, _, num_res = \
        pe.partial_eval_jaxpr_custom(jaxpr, [False, *in_unknowns],
            [True, *in_inst], [], [], saveable)

  # `partial_eval_jaxpr_custom` will give us jaxprs that have hybrid `Ref` and
  # non-Ref input/outputs. However, we'd like to bind these jaxprs to a
  # `for`, which expects only `Ref` inputs and no output. We need to convert
  # both of these jaxprs into ones that are compatible with `for`.
  # TODO(sharadmv,mattjj): implement "passthrough" optimization.
  # TODO(sharadmv,mattjj): rematerialize loop-dependent values instead of
  # passing the loop index as a residual

  # `jaxpr_known_resout` is a jaxpr that maps from all the input `Refs`
  # to output residual values (none of them should be `Ref`s). We'll need to
  # convert the output residual values into `Ref`s that are initially empty
  # `Ref`s that are written to at the end of the jaxpr.

  # # Loop-invariant residual optimization
  # Here we are interested in finding out which of the residuals are *not*
  # dependent on the loop index. If a residual is not dependent on the loop
  # index, we don't need add an extra loop dimension we're reading from when we
  # convert it from an output into a write.
  loop_invar_res = _loop_invariant_outputs(jaxpr_known_resout)

  jaxpr_known, res_avals = _convert_outputs_to_writes(nsteps,
                                                      jaxpr_known_resout,
                                                      loop_invar_res)

  known_invars, _ = partition_list(in_unknowns, eqn.invars)
  known_outvars, _ = partition_list(in_unknowns, eqn.outvars)
  newvar = core.gensym()
  resvars = map(newvar, res_avals)

  @lu.wrap_init
  def known(*known_vals):
    empty_res = map(ad_util.zeros_like_aval, res_avals)
    jaxpr_known_args = [*known_vals, *empty_res]
    jaxpr_known_which_linear = (False,) * len(jaxpr_known_args)
    return for_p.bind(*jaxpr_known_args, jaxpr=jaxpr_known, nsteps=nsteps,
                      reverse=reverse, which_linear=jaxpr_known_which_linear,
                      unroll=unroll)
  call_jaxpr_, _, call_jaxpr_consts, () = pe.trace_to_jaxpr_dynamic(
      known, [v.aval for v in known_invars])
  call_jaxpr = core.ClosedJaxpr(call_jaxpr_, call_jaxpr_consts)
  eqn_known = pe.new_jaxpr_eqn(known_invars, [*known_outvars, *resvars],
                               core.closed_call_p, dict(call_jaxpr=call_jaxpr),
                               call_jaxpr.effects, eqn.source_info)

  jaxpr_staged = _convert_inputs_to_reads(nsteps, len(res_avals),
                                          jaxpr_staged_resin_,
                                          loop_invar_res)
  which_linear_unknown = (False,) * num_res + tuple(which_linear)
  params_staged = dict(eqn.params, jaxpr=jaxpr_staged, reverse=reverse,
                                   nsteps=nsteps,
                                   which_linear=which_linear_unknown,
                                   unroll=unroll)

  @lu.wrap_init
  def staged(*res_and_refs):
    out_flat = for_p.bind(*res_and_refs, **params_staged)
    _, ans = split_list(out_flat, [num_res])
    _, ans = partition_list(out_inst, ans)
    return ans
  call_jaxpr_, _, call_jaxpr_consts, () = pe.trace_to_jaxpr_dynamic(
      staged, [v.aval for v in [*resvars, *eqn.invars]])
  assert len(jaxpr_staged.invars) - 1 == len(call_jaxpr_.invars)
  call_jaxpr = core.ClosedJaxpr(call_jaxpr_, call_jaxpr_consts)
  _, outvars = partition_list(out_inst, eqn.outvars)
  eqn_staged = pe.new_jaxpr_eqn([*resvars, *eqn.invars], outvars,
                               core.closed_call_p, dict(call_jaxpr=call_jaxpr),
                               call_jaxpr.effects, eqn.source_info)
  new_vars = [*new_inst, *resvars]
  return eqn_known, eqn_staged, in_unknowns, out_inst, new_vars
