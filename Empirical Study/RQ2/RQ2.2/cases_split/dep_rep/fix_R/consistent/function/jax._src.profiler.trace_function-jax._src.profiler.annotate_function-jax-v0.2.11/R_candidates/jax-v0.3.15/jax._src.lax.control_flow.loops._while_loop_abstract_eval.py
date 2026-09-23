def _while_loop_abstract_eval(*args, cond_jaxpr, body_jaxpr, **kwargs):
  del args, kwargs
  joined_effects = core.join_effects(cond_jaxpr.effects, body_jaxpr.effects)
  disallowed_effects = joined_effects - allowed_effects
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `while`: {disallowed_effects}')
  return _map(raise_to_shaped, body_jaxpr.out_avals), joined_effects
