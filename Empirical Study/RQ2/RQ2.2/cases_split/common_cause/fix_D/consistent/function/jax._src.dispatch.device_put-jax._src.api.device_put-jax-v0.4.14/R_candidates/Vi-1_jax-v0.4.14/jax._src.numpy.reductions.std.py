@_wraps(np.std, skip_params=['out'])
def std(a: ArrayLike, axis: Axis = None, dtype: DTypeLike = None,
        out: None = None, ddof: int = 0, keepdims: bool = False, *,
        where: Optional[ArrayLike] = None) -> Array:
  return _std(a, _ensure_optional_axes(axis), dtype, out, ddof, keepdims,
              where=where)
