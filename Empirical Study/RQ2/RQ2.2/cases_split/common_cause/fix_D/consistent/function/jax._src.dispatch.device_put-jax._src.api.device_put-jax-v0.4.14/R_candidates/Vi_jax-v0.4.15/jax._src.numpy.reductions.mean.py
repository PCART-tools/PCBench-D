@_wraps(np.mean, skip_params=['out'])
def mean(a: ArrayLike, axis: Axis = None, dtype: DTypeLike = None,
         out: None = None, keepdims: bool = False, *,
         where: Optional[ArrayLike] = None) -> Array:
  return _mean(a, _ensure_optional_axes(axis), dtype, out, keepdims,
               where=where)
