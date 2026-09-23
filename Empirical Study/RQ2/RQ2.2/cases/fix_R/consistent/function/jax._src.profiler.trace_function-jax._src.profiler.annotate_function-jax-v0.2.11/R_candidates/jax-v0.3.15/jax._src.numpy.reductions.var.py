@_wraps(np.var, skip_params=['out'])
def var(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype=None,
        out=None, ddof=0, keepdims=False, *, where=None):
  return _var(a, _ensure_optional_axes(axis), dtype, out, ddof, keepdims,
              where=where)
