def _for_partial_eval(trace: pe.JaxprTrace, *tracers: pe.JaxprTracer,
                      jaxpr: core.Jaxpr, nsteps: int, reverse: bool,
                      which_linear: Tuple[bool]) -> List[pe.JaxprTracer]:
  num_inputs = len(tracers)
  in_unknowns = [not t.pval.is_known() for t in tracers]
  # We first need to run a fixpoint to determine which of the `Ref`s are unknown
  # after running the for loop. We want to use the jaxpr to determine which
  # `Ref`s are unknown after executing the for loop body given which `Ref`s are
  # unknown before. However, the jaxpr has no outputs. Instead, we discharge
  # the body and run the fixpoint with the discharged jaxpr. We can do this
  # because the outputs of the jaxpr are one-to-one with the inputs.
  discharged_jaxpr, discharged_consts = discharge_state(jaxpr, ())
  discharged_jaxpr = discharged_jaxpr.replace(
      invars=discharged_jaxpr.constvars + discharged_jaxpr.invars,
      constvars=[])
  for _ in range(num_inputs):
    jaxpr_in_unknowns = [False] * len(discharged_consts) + [False, *in_unknowns]
    _, _, out_unknowns, _, _ = _partial_eval_jaxpr_custom(
        discharged_jaxpr, jaxpr_in_unknowns, _save_everything)
    out_unknowns = list(out_unknowns)
    if out_unknowns == in_unknowns:
      break
    in_unknowns = map(operator.or_, in_unknowns, out_unknowns)
  else:
    raise Exception("Invalid fixpoint")
  del out_unknowns  # redundant since it's the same as `in_unknowns`
  tracers = tuple(trace.instantiate_const(t) if uk else t
                  for t, uk in zip(tracers, in_unknowns))

  # We use `partial_eval_jaxpr_custom` here because it won't remove effectful
  # primitives like `get`/`set`.
  jaxpr_known_resout, jaxpr_unknown_resin_, _, _, num_res = \
        _partial_eval_jaxpr_custom(jaxpr, [False, *in_unknowns],
                                   _save_everything)
  # `partial_eval_jaxpr_custom` will give us jaxprs that have hybrid `Ref` and
  # regular valued input/outputs. However, we'd like to bind these jaxprs to a
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

  # In order to detect which residuals are loop-invariant, we need to run a
  # fixpoint. This is because the residual could be dependent on a `Ref` that
  # changes each iteration of the loop so we need to first detect which `Ref`s
  # are loop-varying. We can do this by discharging the state from the jaxpr and
  # running partial_eval with initially only the loop-index being loop-varying.
  # The fixpoint will eventually propagate the loop-varying-ness over the
  # inputs/outputs and we will converge.
  loop_var_res = [False] * len(jaxpr_known_resout.outvars)
  loop_var_refs = [False] * (len(jaxpr_known_resout.invars) - 1)
  discharged_jaxpr_known_resout = core.ClosedJaxpr(
      *discharge_state(jaxpr_known_resout, ()))
  for _ in range(len(discharged_jaxpr_known_resout.jaxpr.invars)):
    (_, _, loop_var_outputs, _) = pe.partial_eval_jaxpr_nounits(
          discharged_jaxpr_known_resout, [True] + loop_var_refs, False)
    loop_var_res, loop_var_refs_ = split_list(
        loop_var_outputs, [len(loop_var_res)])
    if loop_var_refs == loop_var_refs_:
      break
    loop_var_refs = map(operator.or_, loop_var_refs, loop_var_refs_)
  # Now that the fixpoint is complete, we know which residuals are
  # loop-invariant.
  loop_invar_res = map(operator.not_, loop_var_res)

  jaxpr_known, res_avals = _convert_outputs_to_writes(nsteps,
                                                      jaxpr_known_resout,
                                                      loop_invar_res)
  # We now run the known jaxpr to obtain our residual values.
  known_tracers, _ = partition_list(in_unknowns, tracers)
  known_vals = [t.pval.get_known() for t in known_tracers]
  empty_res = map(ad_util.zeros_like_aval, res_avals)
  jaxpr_known_args = [*known_vals, *empty_res]
  jaxpr_known_which_linear = (False,) * len(jaxpr_known_args)
  out_flat = for_p.bind(*jaxpr_known_args, jaxpr=jaxpr_known, nsteps=nsteps,
                        reverse=reverse, which_linear=jaxpr_known_which_linear)
  known_outputs, residuals = split_list(out_flat, [len(known_tracers)])
  residuals = map(trace.new_instantiated_const, residuals)

  # Now we handle the `jaxpr_unknown` that expects residual values as inputs.
  # This jaxpr is the output of `partial_eval_jaxpr_custom` that marks which
  # inputs are actually used.
  # `partial_eval_jaxpr_custom` doesn't remove extra inputs/outputs for you
  # so we use `dce_jaxpr` here to do that.
  jaxpr_unknown_resin, used_inputs = pe.dce_jaxpr(
        jaxpr_unknown_resin_, [], [True] * num_res + [True, *in_unknowns])
  used_res, (used_i,), used_refs = split_list(used_inputs, [num_res, 1])
  assert all(used_res), "All residuals should be used"
  # To make it compatible with `for`, we need to convert those residual values
  # into `Ref`s.
  jaxpr_unknown = _convert_inputs_to_reads(nsteps, len(res_avals),
                                           jaxpr_unknown_resin,
                                           loop_invar_res)
  # Since not all inputs are used in jaxpr_unknown, we filter the input tracers
  # down using the output of `dce_jaxpr`.
  _, used_tracers = partition_list(used_refs, tracers)
  _, used_which_linear = partition_list(used_refs, which_linear)
  which_linear_unknown = (False,) * num_res + tuple(used_which_linear)
  unknown_inputs = [*residuals, *used_tracers]
  # Outputs match inputs so we construct output tracers that look like the input
  # tracers.
  res_ref_unknown_outputs = [
      pe.JaxprTracer(trace, pe.PartialVal.unknown(t.aval), None)
      for t in unknown_inputs]
  name_stack = source_info_util.current_name_stack()[len(trace.name_stack):]
  source = source_info_util.current().replace(name_stack=name_stack)

  eqn = pe.new_eqn_recipe(unknown_inputs, res_ref_unknown_outputs,
                          for_p, dict(jaxpr=jaxpr_unknown, nsteps=nsteps,
                                      reverse=reverse,
                                      which_linear=which_linear_unknown),
                          core.no_effects, source)
  _, unknown_outputs = split_list(res_ref_unknown_outputs, [num_res])
  for t in unknown_outputs: t.recipe = eqn
  return merge_lists(in_unknowns, known_outputs, unknown_outputs)
