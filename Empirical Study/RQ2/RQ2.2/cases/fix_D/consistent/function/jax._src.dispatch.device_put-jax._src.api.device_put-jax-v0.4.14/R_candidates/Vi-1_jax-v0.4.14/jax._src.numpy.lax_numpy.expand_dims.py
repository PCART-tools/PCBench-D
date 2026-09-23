@util._wraps(np.expand_dims)
def expand_dims(a: ArrayLike, axis: Union[int, Sequence[int]]) -> Array:
  util.check_arraylike("expand_dims", a)
  axis = _ensure_index_tuple(axis)
  return lax.expand_dims(a, axis)
