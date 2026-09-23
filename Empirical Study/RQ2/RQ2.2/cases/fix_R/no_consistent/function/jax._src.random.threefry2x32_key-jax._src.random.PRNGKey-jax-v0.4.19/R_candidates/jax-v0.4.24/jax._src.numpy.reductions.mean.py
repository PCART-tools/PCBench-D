@implements(np.mean, skip_params=['out'])
def mean(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
         out: None = None, keepdims: bool = False, *,
         where: ArrayLike | None = None) -> Array:
  return _mean(a, _ensure_optional_axes(axis), dtype, out, keepdims,
               where=where)
