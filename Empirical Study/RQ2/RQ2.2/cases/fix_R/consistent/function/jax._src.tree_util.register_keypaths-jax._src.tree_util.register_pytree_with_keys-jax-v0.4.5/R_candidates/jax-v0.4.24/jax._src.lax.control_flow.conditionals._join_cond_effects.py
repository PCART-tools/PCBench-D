def _join_cond_effects(branches: Sequence[core.Jaxpr]) -> effects.Effects:
  joined_effects = set()
  for b in branches:
    for eff in b.effects:
      if isinstance(eff, effects.JaxprInputEffect):
        # Offset index to handle predicate
        eff = eff.replace(input_index=eff.input_index + 1)
      joined_effects.add(eff)
  return joined_effects
