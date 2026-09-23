def _canonicalize_tuple_index(arr_ndim, idx, array_name='array'):
  """Helper to remove Ellipsis and add in the implicit trailing slice(None)."""
  num_dimensions_consumed = sum(not (e is None or e is Ellipsis or isinstance(e, bool)) for e in idx)
  if num_dimensions_consumed > arr_ndim:
    raise IndexError(
        f"Too many indices for {array_name}: {num_dimensions_consumed} "
        f"non-None/Ellipsis indices for dim {arr_ndim}.")
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
