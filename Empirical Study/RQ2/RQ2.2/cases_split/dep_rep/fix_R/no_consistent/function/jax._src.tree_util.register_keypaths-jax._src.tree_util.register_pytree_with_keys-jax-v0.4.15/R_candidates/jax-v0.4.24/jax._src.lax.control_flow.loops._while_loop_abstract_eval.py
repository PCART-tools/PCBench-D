def _while_loop_abstract_eval(*avals, cond_jaxpr, body_jaxpr, body_nconsts,
                              cond_nconsts):
  del avals
  joined_effects = _join_while_effects(body_jaxpr, cond_jaxpr, body_nconsts,
                                       cond_nconsts)
  disallowed_effects = effects.control_flow_allowed_effects.filter_not_in(joined_effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `while`: {disallowed_effects}')
  return _map(raise_to_shaped, body_jaxpr.out_avals), joined_effects
