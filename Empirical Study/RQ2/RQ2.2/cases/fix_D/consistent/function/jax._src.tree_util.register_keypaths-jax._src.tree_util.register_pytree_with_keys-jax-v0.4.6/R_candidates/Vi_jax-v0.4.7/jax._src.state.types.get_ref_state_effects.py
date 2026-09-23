def get_ref_state_effects(
    avals: Sequence[core.AbstractValue],
    effects: core.Effects) -> List[Set[StateEffect]]:
  return [{eff for eff in effects
           if isinstance(eff, (ReadEffect, WriteEffect, AccumEffect))
           and eff.input_index == i} for i, _ in enumerate(avals)]
