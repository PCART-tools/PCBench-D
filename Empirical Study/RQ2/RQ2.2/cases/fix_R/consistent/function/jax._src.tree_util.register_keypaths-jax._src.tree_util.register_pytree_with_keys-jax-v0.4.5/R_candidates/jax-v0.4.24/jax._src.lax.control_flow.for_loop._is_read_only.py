def _is_read_only(ref_effects: set[StateEffect]) -> bool:
  assert len(ref_effects) > 0
  if len(ref_effects) > 1:
    # Means we must have a write or accum effect so not read-only
    return False
  eff, = ref_effects
  return isinstance(eff, ReadEffect)
