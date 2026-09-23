@util._wraps(np.expand_dims)
def expand_dims(a: ArrayLike, axis: Union[int, Sequence[int]]) -> Array:
  util._stackable(a) or util._check_arraylike("expand_dims", a)
  axis = _ensure_index_tuple(axis)
  if hasattr(a, "expand_dims"):
    return a.expand_dims(axis)  # type: ignore
  return lax.expand_dims(a, axis)
