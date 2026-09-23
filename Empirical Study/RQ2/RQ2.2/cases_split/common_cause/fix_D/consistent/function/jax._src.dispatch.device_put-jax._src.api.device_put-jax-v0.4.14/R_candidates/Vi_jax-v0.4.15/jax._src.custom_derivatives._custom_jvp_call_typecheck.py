def _custom_jvp_call_typecheck(_, *in_avals, call_jaxpr, jvp_jaxpr_thunk,
                               num_consts, symbolic_zeros):
  # TODO(mattjj): could do more checking here...
  del in_avals, jvp_jaxpr_thunk, num_consts
  disallowed_effects = allowed_effects.filter_not_in(call_jaxpr.effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `custom_jvp`: {disallowed_effects}')
  return call_jaxpr.out_avals, call_jaxpr.effects
