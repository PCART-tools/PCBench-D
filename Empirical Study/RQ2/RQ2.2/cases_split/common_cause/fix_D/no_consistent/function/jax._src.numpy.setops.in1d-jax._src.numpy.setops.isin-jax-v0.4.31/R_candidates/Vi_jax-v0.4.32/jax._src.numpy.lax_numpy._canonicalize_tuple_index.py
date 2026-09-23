def _canonicalize_tuple_index(arr_ndim, idx):
  """Helper to remove Ellipsis and add in the implicit trailing slice(None)."""
  num_dimensions_consumed = sum(not (e is None or e is Ellipsis or isinstance(e, bool)) for e in idx)
  if num_dimensions_consumed > arr_ndim:
    index_or_indices = "index" if num_dimensions_consumed == 1 else "indices"
    raise IndexError(
        f"Too many indices: {arr_ndim}-dimensional array indexed "
        f"with {num_dimensions_consumed} regular {index_or_indices}.")
  ellipses = (i for i, elt in enumerate(idx) if elt is Ellipsis)
  ellipsis_index = next(ellipses, None)
  if ellipsis_index is not None:
    if next(ellipses, None) is not None:
      raise IndexError(
          f"Multiple ellipses (...) not supported: {list(map(type, idx))}.")
    colons = (slice(None),) * (arr_ndim - num_dimensions_consumed)
    idx = idx[:ellipsis_index] + colons + idx[ellipsis_index + 1:]
  elif num_dimensions_consumed < arr_ndim:
    colons = (slice(None),) * (arr_ndim - num_dimensions_consumed)
    idx = tuple(idx) + colons
  return idx
