def _prepend_scatter(x, indexer, val, *, add=False):
  # NumPy advanced int indexing won't prepend w/ only one dim, so add dummy.
  # However, since this is scatter, we need to remove the 1-sized dimension
  # we added at the front.
  if add:
    return x[None].at[(0, *indexer)].add(val)[0]
  return x[None].at[(0, *indexer)].set(val)[0]
