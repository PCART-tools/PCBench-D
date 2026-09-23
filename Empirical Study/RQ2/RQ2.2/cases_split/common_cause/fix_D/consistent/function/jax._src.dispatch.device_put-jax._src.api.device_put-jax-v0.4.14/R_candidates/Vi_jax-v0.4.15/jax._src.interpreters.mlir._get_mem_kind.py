def _get_mem_kind(s: Optional[XLACompatibleSharding]) -> Optional[str]:
  if s is None:
    return None
  assert isinstance(s, sharding_impls.XLACompatibleSharding)
  return s.memory_kind
