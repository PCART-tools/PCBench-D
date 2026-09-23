@_wraps(np.unravel_index, lax_description=_UNRAVEL_INDEX_DOC)
def unravel_index(indices, shape):
  _check_arraylike("unravel_index", indices)
  # Note: we do not convert shape to an array, because it may be passed as a
  # tuple of weakly-typed values, and asarray() would strip these weak types.
  try:
    shape = list(shape)
  except TypeError:
    shape = [shape]
  if _any(ndim(s) != 0 for s in shape):
    raise ValueError("unravel_index: shape should be a scalar or 1D sequence.")
  out_indices = [None] * len(shape)
  for i, s in reversed(list(enumerate(shape))):
    indices, out_indices[i] = divmod(indices, s)
  oob_pos = indices > 0
  oob_neg = indices < -1
  return tuple(where(oob_pos, s - 1, where(oob_neg, 0, i))
               for s, i in zip(shape, out_indices))
