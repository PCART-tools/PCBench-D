@_wraps(np.max, skip_params=['out'])
def max(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, initial: Optional[ArrayLike] = None,
        where: Optional[ArrayLike] = None) -> Array:
  return _reduce_max(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, initial=initial, where=where)
