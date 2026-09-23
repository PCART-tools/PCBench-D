def _is_trivial_indexer(indexer: indexing.NDIndexer):
  for s, idx in zip(indexer.shape, indexer.indices):
    if not isinstance(idx, indexing.Slice):
      return False
    if not isinstance(idx.start, int):
      return False
    if idx.start:
      return False
    if idx.size != s:
      return False
  return True
