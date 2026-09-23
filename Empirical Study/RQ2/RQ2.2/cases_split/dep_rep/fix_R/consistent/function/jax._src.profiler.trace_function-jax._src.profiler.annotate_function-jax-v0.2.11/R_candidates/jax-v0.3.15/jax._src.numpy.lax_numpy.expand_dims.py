@_wraps(np.expand_dims)
def expand_dims(a, axis: Union[int, Sequence[int]]):
  _stackable(a) or _check_arraylike("expand_dims", a)
  axis = _ensure_index_tuple(axis)
  if hasattr(a, "expand_dims"):
    return a.expand_dims(axis)
  return lax.expand_dims(a, axis)
