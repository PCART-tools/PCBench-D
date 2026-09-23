def _canonicalize_tuple_index(arr_ndim, idx, array_name='array'):
  """Helper to remove Ellipsis and add in the implicit trailing slice(None)."""
  len_without_none = sum(e is not None and e is not Ellipsis for e in idx)
  if len_without_none > arr_ndim:
    raise IndexError(
        f"Too many indices for {array_name}: {len_without_none} "
        f"non-None/Ellipsis indices for dim {arr_ndim}.")
  ellipses = (i for i, elt in enumerate(idx) if elt is Ellipsis)
  ellipsis_index = next(ellipses, None)
  if ellipsis_index is not None:
    if next(ellipses, None) is not None:
      raise IndexError(
          f"Multiple ellipses (...) not supported: {list(map(type, idx))}.")
    colons = (slice(None),) * (arr_ndim - len_without_none)
    idx = idx[:ellipsis_index] + colons + idx[ellipsis_index + 1:]
  elif len_without_none < arr_ndim:
    colons = (slice(None),) * (arr_ndim - len_without_none)
    idx = tuple(idx) + colons
  return idx
