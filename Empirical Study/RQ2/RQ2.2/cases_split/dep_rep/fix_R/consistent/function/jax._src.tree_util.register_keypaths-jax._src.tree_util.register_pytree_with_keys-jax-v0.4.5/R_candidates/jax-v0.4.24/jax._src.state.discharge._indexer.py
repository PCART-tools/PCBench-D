def _indexer(idx, indexed_dims):
  idx_ = iter(idx)
  indexer = tuple(next(idx_) if b else slice(None) for b in indexed_dims)
  assert next(idx_, None) is None
  return indexer
