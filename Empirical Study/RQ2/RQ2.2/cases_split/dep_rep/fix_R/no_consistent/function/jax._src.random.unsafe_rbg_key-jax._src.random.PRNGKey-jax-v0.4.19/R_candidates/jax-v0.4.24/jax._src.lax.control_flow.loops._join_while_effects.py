def _join_while_effects(body_jaxpr, cond_jaxpr, body_nconsts, cond_nconsts
                       ) -> effects.Effects:
  joined_effects = set()
  for eff in cond_jaxpr.effects:
    if isinstance(eff, effects.JaxprInputEffect):
      index = eff.input_index
      if index >= cond_nconsts:
        index += body_nconsts
      eff = eff.replace(input_index=index)
    joined_effects.add(eff)
  for eff in body_jaxpr.effects:
    if isinstance(eff, effects.JaxprInputEffect):
      index = eff.input_index + cond_nconsts
      eff = eff.replace(input_index=index)
    joined_effects.add(eff)
  return joined_effects
