def _prepend_gather(x, idx, indexed_dims):
  indexer = _indexer(idx, indexed_dims)
  # NumPy advanced int indexing won't prepend w/ only one dim, so add dummy.
  return x[None][(np.array(0, 'int32'), *indexer)]
