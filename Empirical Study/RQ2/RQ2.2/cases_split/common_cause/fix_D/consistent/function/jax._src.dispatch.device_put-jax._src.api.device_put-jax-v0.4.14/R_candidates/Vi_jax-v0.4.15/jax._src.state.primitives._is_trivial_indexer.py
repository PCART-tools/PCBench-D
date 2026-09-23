def _is_trivial_indexer(idx: Indexer) -> bool:
  if idx is ...:
    return True
  if type(idx) is tuple:
    if len(idx) == 0:
      return True
    return len(idx) == 1 and idx[0] is ...
  return False
