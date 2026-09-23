def _cond_abstract_eval(*args, branches, **kwargs):
  joined_effects = core.join_effects(*(b.effects for b in branches))
  disallowed_effects = joined_effects - allowed_effects
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `cond`: {disallowed_effects}')
  joined_effects = core.join_effects(*(b.effects for b in branches))
  return _map(raise_to_shaped, branches[0].out_avals), joined_effects
