def _is_advanced_int_indexer(idx):
  """Returns True if idx should trigger int array indexing, False otherwise."""
  # https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html#advanced-indexing
  assert isinstance(idx, tuple)
  if all(e is None or e is Ellipsis or isinstance(e, slice)
         or _is_scalar(e) and issubdtype(_dtype(e), np.integer) for e in idx):
    return False
  return all(e is None or e is Ellipsis or isinstance(e, slice)
             or _is_int_arraylike(e) for e in idx)
