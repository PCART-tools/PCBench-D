@_wraps(np.min, skip_params=['out'])
def min(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, initial: Optional[ArrayLike] = None,
        where: Optional[ArrayLike] = None) -> Array:
  return _reduce_min(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, initial=initial, where=where)
