@_wraps(np.argmin, skip_params=['out'])
def argmin(a, axis: Optional[int] = None, out=None, keepdims=None):
  return _argmin(a, None if axis is None else operator.index(axis), keepdims=bool(keepdims))
