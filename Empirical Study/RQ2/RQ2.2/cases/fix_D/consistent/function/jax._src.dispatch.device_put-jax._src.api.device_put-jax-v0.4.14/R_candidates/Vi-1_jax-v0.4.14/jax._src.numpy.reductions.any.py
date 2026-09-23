@_wraps(np.any, skip_params=['out'])
def any(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, *, where: Optional[ArrayLike] = None) -> Array:
  return _reduce_any(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, where=where)
