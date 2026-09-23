@_wraps(np.all, skip_params=['out'])
def all(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, *, where: Optional[ArrayLike] = None) -> Array:
  return _reduce_all(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, where=where)
