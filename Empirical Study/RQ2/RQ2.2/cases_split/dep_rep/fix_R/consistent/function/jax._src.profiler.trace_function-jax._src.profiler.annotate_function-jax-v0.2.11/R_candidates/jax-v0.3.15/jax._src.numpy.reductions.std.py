@_wraps(np.std, skip_params=['out'])
def std(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype=None,
        out=None, ddof=0, keepdims=False, *, where=None):
  return _std(a, _ensure_optional_axes(axis), dtype, out, ddof, keepdims,
              where=where)
