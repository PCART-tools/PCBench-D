def _prepend_scatter(x, idx, indexed_dims, val, *, add=False):
  indexer = _indexer(idx, indexed_dims)
  if add:
    return x[None].at[(0, *indexer)].add(val)[0]
  return x[None].at[(0, *indexer)].set(val)[0]
