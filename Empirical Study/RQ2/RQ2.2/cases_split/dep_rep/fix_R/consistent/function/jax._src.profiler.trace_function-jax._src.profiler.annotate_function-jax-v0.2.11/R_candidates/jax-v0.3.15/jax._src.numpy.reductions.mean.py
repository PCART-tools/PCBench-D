@_wraps(np.mean, skip_params=['out'])
def mean(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype=None,
         out=None, keepdims=False, *, where=None):
  return _mean(a, _ensure_optional_axes(axis), dtype, out, keepdims,
               where=where)
