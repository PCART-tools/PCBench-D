def _cond_abstract_eval(*avals, branches, **_):
  joined_effects = _join_cond_effects(branches)
  disallowed_effects = allowed_effects.filter_not_in(joined_effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `cond`: {disallowed_effects}')
  return map(raise_to_shaped, branches[0].out_avals), joined_effects
