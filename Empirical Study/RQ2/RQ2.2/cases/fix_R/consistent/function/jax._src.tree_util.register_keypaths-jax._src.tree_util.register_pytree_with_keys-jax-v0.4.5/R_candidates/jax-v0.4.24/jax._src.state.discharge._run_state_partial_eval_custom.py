def _run_state_partial_eval_custom(
    saveable: Callable[..., pe.RematCases_],
    in_unknowns: Sequence[bool],
    in_inst: Sequence[bool],
    eqn: core.JaxprEqn):
  if not any(in_unknowns):
    return eqn, None, in_unknowns, [False] * len(in_unknowns), []
  jaxpr, which_linear = split_dict(eqn.params, ["jaxpr", "which_linear"])
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
  out_unknowns, out_inst =  in_unknowns, in_unknowns
  for _ in range(num_inputs):
    jaxpr_in_unknowns = [False] * len(discharged_consts) + in_unknowns
    _, _, out_unknowns, out_inst, _, _ = pe.partial_eval_jaxpr_stateful(
        discharged_jaxpr,
        in_unknowns=jaxpr_in_unknowns,
        in_inst=jaxpr_in_unknowns,
        ensure_out_unknowns=in_unknowns,
        ensure_out_inst=in_unknowns,
        saveable=saveable)
    out_unknowns = list(out_unknowns)
    if out_unknowns == in_unknowns:
      break
    in_unknowns = map(operator.or_, in_unknowns, out_unknowns)
  else:
    if num_inputs > 0: raise Exception("Invalid fixpoint")
  del out_unknowns # Redundant since it's the same as `in_unknowns`
  new_inst = [x for x, already, inst in zip(eqn.invars, in_inst, out_inst)
              if type(x) is core.Var and inst and not already]

  # We use `partial_eval_jaxpr_stateful` here because it won't remove effectful
  # primitives like `get`/`set`.
  jaxpr_known_resout, jaxpr_staged_resin_, _, _, num_res_out, num_res_ref = \
        pe.partial_eval_jaxpr_stateful(jaxpr, in_unknowns,
            in_unknowns, [], [], saveable)
  num_res = num_res_ref + num_res_out
  # `partial_eval_jaxpr_stateful` will give us jaxprs that have hybrid `Ref` and
  # non-Ref input/outputs. However, we'd like to bind these jaxprs to a
  # `for`, which expects only `Ref` inputs and no output. We need to convert
  # both of these jaxprs into ones that are compatible with `for`.
  # TODO(sharadmv,mattjj): implement "passthrough" optimization.

  # `jaxpr_known_resout` is a jaxpr that maps from all the input `Refs`
  # to output residual values (none of them should be `Ref`s). We'll need to
  # convert the output residual values into `Ref`s that are initially empty
  # `Ref`s that are written to at the end of the jaxpr.
  jaxpr_known, res_avals = _convert_outputs_to_writes(jaxpr_known_resout)

  # In a stateful partial_eval, the residuals should be `Ref`s.
  res_avals = map(AbstractRef, res_avals)  # type: ignore

  known_invars, staged_invars = partition_list(in_unknowns, eqn.invars)
  known_outvars, staged_outvars = partition_list(in_unknowns, eqn.outvars)
  newvar = core.gensym()
  _, res_ref_avals = split_list([v.aval for v in jaxpr_known_resout.invars],
                                [len(known_invars)])
  nonref_resvars = map(newvar, res_avals)
  ref_resvars = map(newvar, res_ref_avals)
  known_out_resvars = map(newvar, [*res_ref_avals, *res_avals])

  known_which_linear, _ = partition_list(in_unknowns, which_linear)
  jaxpr_known_which_linear = (*known_which_linear, *(False,) * num_res)
  known_and_res_invars = [*known_invars, *ref_resvars, *nonref_resvars]

  known_params = dict(jaxpr=jaxpr_known, which_linear=jaxpr_known_which_linear)
  _, known_effects = run_state_p.abstract_eval(
      *[v.aval for v in known_and_res_invars], **known_params)
  eqn_known = pe.new_jaxpr_eqn(known_and_res_invars,
                               [*known_outvars, *known_out_resvars],
                               run_state_p, known_params,
                               known_effects, eqn.source_info)

  jaxpr_staged = _convert_inputs_to_reads(len(res_avals), jaxpr_staged_resin_)

  _, staged_which_linear = partition_list(in_unknowns, which_linear)
  which_linear_unknown = (*[False] * num_res, *staged_which_linear)
  staged_params = dict(jaxpr=jaxpr_staged, which_linear=which_linear_unknown)
  rejiggered_resvars = [*nonref_resvars, *ref_resvars]
  _, staged_invars = partition_list(in_unknowns, eqn.invars)
  res_staged_invars = [*rejiggered_resvars, *staged_invars]
  _, staged_effects = run_state_p.abstract_eval(
      *[v.aval for v in res_staged_invars], **staged_params)
  _, staged_outvars = partition_list(in_unknowns, eqn.outvars)
  if num_res:
    @lu.wrap_init
    def staged(*args):
      out = run_state_p.bind(*args, **staged_params)
      return out[num_res:]
    staged_call_jaxpr, _, (), () = pe.trace_to_jaxpr_dynamic(staged,
        [v.aval for v in res_staged_invars])
    eqn_staged = pe.new_jaxpr_eqn(res_staged_invars,
                                  staged_outvars,
                                  core.closed_call_p,
                                  dict(call_jaxpr=pe.close_jaxpr(staged_call_jaxpr)),
                                  staged_effects, eqn.source_info)
    assert len(res_staged_invars) == len(staged_call_jaxpr.invars)
    assert len(staged_outvars) == len(staged_call_jaxpr.outvars)
  else:
    eqn_staged = pe.new_jaxpr_eqn(staged_invars,
                                  staged_outvars,
                                  run_state_p,
                                  staged_params,
                                  staged_effects, eqn.source_info)
  new_vars = [*new_inst, *nonref_resvars, *ref_resvars]
  return eqn_known, eqn_staged, in_unknowns, in_unknowns, new_vars
