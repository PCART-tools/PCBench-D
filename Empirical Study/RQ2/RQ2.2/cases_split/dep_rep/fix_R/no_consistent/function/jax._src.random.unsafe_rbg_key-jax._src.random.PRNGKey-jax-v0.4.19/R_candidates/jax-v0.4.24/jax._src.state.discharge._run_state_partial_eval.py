def _run_state_partial_eval(trace: pe.JaxprTrace, *tracers: pe.JaxprTracer,
                            jaxpr: core.Jaxpr, which_linear: tuple[bool, ...]):
  num_inputs = len(tracers)
  assert num_inputs == len(jaxpr.invars)
  in_unknowns = [not t.pval.is_known() for t in tracers]
  # We first need to run a fixpoint to determine which of the `Ref`s are unknown
  # after running the for loop. We want to use the jaxpr to determine which
  # `Ref`s are unknown after executing the for loop body given which `Ref`s are
  # unknown before. However, the jaxpr has no outputs. Instead, we discharge
  # the body and run the fixpoint with the discharged jaxpr. We can do this
  # because the outputs of the jaxpr are one-to-one with the inputs.
  discharged_jaxpr_, discharged_consts = discharge_state(jaxpr, ())
  discharged_jaxpr = pe.convert_constvars_jaxpr(discharged_jaxpr_)
  for _ in range(num_inputs):
    jaxpr_in_unknowns = [False] * len(discharged_consts) + in_unknowns
    _, _, out_unknowns, out_inst, _, _ = pe.partial_eval_jaxpr_stateful(
        discharged_jaxpr, jaxpr_in_unknowns, jaxpr_in_unknowns,
          in_unknowns, False, _save_everything)
    # assert out_inst == out_unknowns
    out_unknowns = list(out_unknowns)
    if out_unknowns == in_unknowns:
      break
    in_unknowns = map(operator.or_, in_unknowns, out_unknowns)
  else:
    raise Exception("Invalid fixpoint")
  del out_unknowns  # redundant since it's the same as `in_unknowns`
  tracers = tuple(trace.instantiate_const(t) if uk else t  # type: ignore
                  for t, uk in zip(tracers, in_unknowns))

  # We use `partial_eval_jaxpr_stateful` here because it won't remove effectful
  # primitives like `get`/`set`.
  jaxpr_known_resout, jaxpr_unknown_resin_, _, _, num_res_out, num_res_ref = \
        pe.partial_eval_jaxpr_stateful(jaxpr, in_unknowns, in_inst=in_unknowns,
                                     ensure_out_unknowns=[], ensure_out_inst=[],
                                     saveable=_save_everything)
  # # `partial_eval_jaxpr_stateful` will give us jaxprs that have hybrid `Ref`
  # and regular valued input/outputs. However, we'd like to bind these jaxprs to
  # a `for`, which expects only `Ref` inputs and no output. We need to convert
  # both of these jaxprs into ones that are compatible with `for`.

  # `jaxpr_known_resout` is a jaxpr that maps from all the input `Refs`
  # to output residual values (none of them should be `Ref`s). We'll need to
  # convert the output residual values into `Ref`s that are initially empty
  # `Ref`s that are written to at the end of the jaxpr.
  num_res = num_res_out + num_res_ref

  num_invars = len(jaxpr_known_resout.invars) - num_res_ref
  _, res_ref_avals = split_list(
      [v.aval for v in jaxpr_known_resout.invars], [num_invars])
  res_avals = [a.inner_aval for a in res_ref_avals]  # pytype: disable=attribute-error
  jaxpr_known, new_res_avals = _convert_outputs_to_writes(jaxpr_known_resout)
  # We now run the known jaxpr to obtain our residual values.
  known_tracers, _ = partition_list(in_unknowns, tracers)
  known_which_linear, _ = partition_list(in_unknowns, which_linear)
  known_vals = [t.pval.get_known() for t in known_tracers]
  all_res_avals = [*res_avals, *new_res_avals]
  empty_res = map(ad_util.zeros_like_aval, all_res_avals)
  jaxpr_known_args = [*known_vals, *empty_res]

  jaxpr_known_which_linear = (*known_which_linear, *(False,) * num_res)
  out_flat = run_state_p.bind(*jaxpr_known_args, jaxpr=jaxpr_known,
                              which_linear=jaxpr_known_which_linear)
  known_outputs, residuals = split_list(out_flat, [len(known_tracers)])
  residuals = map(trace.new_instantiated_const, residuals)
  ref_res, nonref_res = split_list(residuals, [num_res_ref])

  # Now we handle the `jaxpr_unknown` that expects residual values as inputs.
  # This jaxpr is the output of `partial_eval_jaxpr_stateful` that marks which
  # inputs are actually used.
  # `partial_eval_jaxpr_stateful` doesn't remove extra inputs/outputs for you
  # so we use `dce_jaxpr` here to do that.
  # To make it compatible with `for`, we need to convert those residual values
  # into `Ref`s.
  jaxpr_unknown = _convert_inputs_to_reads(len(new_res_avals),
                                           jaxpr_unknown_resin_)
  _, unknown_tracers = partition_list(in_unknowns, tracers)
  _, uk_which_linear = partition_list(in_unknowns, which_linear)
  unknown_which_linear = (False,) * num_res + tuple(uk_which_linear)
  unknown_inputs = [*nonref_res, *ref_res, *unknown_tracers]
  # Outputs match inputs so we construct output tracers that look like the input
  # tracers.
  res_ref_unknown_outputs = [
      pe.JaxprTracer(trace, pe.PartialVal.unknown(t.aval), None)
      for t in unknown_inputs]
  name_stack = source_info_util.current_name_stack()[len(trace.name_stack):]
  source = source_info_util.current().replace(name_stack=name_stack)

  assert len(unknown_inputs) == len(res_ref_unknown_outputs)
  assert len(unknown_inputs) == len(jaxpr_unknown.invars)
  uk_params = dict(jaxpr=jaxpr_unknown, which_linear=unknown_which_linear)
  _, eqn_effects = run_state_p.abstract_eval(*[v.aval for v in unknown_inputs],
                                             **uk_params)
  eqn = pe.new_eqn_recipe(unknown_inputs, res_ref_unknown_outputs,
                          run_state_p, uk_params,
                          eqn_effects, source)
  for t in res_ref_unknown_outputs: t.recipe = eqn
  _, unknown_outputs = split_list(res_ref_unknown_outputs, [num_res])
  return merge_lists(in_unknowns, known_outputs, unknown_outputs)
