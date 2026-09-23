def _prepend_gather(x, indexer):
  # NumPy advanced int indexing won't prepend w/ only one dim, so add dummy.
  return x[None][(np.array(0, 'int32'), *indexer)]
