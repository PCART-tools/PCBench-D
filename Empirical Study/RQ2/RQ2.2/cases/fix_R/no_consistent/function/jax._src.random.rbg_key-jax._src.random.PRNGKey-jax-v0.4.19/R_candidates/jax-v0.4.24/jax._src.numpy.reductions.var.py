@implements(np.var, skip_params=['out'])
def var(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
        out: None = None, ddof: int = 0, keepdims: bool = False, *,
        where: ArrayLike | None = None) -> Array:
  return _var(a, _ensure_optional_axes(axis), dtype, out, ddof, keepdims,
              where=where)
