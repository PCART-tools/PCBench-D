def _get_mem_kind(s: XLACompatibleSharding | None) -> str | None:
  if s is None:
    return None
  assert isinstance(s, sharding_impls.XLACompatibleSharding)
  return s.memory_kind
