def _loop_invariant_outputs(jaxpr: core.Jaxpr) -> List[bool]:
  # Get effects for each of the jaxpr inputs and remove the loop index.
  ref_effects = state.get_ref_state_effects(
      [v.aval for v in jaxpr.invars], jaxpr.effects)[1:]
  # We first assume that *read-only `Ref`s* are loop-invariant. We can safely do
  # this because the only way something can be loop-varying is if we write to it
  # at some point. It's *possible* that read-write `Ref`s are loop-invariant but
  # we conservatively assume they aren't.
  loop_invar_refs = [_is_read_only(effs) if effs else True
                     for effs in ref_effects]
  loop_var_refs = map(operator.not_, loop_invar_refs)

  # We'd like to detect if the outputs of the jaxpr are loop-invariant. An
  # output is loop-invariant if it is downstream of only loop-invariant values
  # (seeded by the read-only `Ref`s). If at any point, a loop-varying value
  # interacts with a loop-invariant value, we produce a loop-varying value. We
  # can use `partial_eval` to perform this analysis by treating loop-varying
  # values as "unknown" and loop-invariant values as "known", since when a known
  # and unknown value interact, they produce an unknown value.
  loop_var_inputs = [True, *loop_var_refs]
  _, _, loop_var_outputs, _, _, = _partial_eval_jaxpr_custom(
      jaxpr, loop_var_inputs, _save_everything)
  return map(operator.not_, loop_var_outputs)
