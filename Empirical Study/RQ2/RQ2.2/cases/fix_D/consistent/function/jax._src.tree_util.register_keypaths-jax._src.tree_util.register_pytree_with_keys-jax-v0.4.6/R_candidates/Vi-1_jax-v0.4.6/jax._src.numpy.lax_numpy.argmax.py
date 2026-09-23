@util._wraps(np.argmax, skip_params=['out'])
def argmax(a, axis: Optional[int] = None, out=None, keepdims=None):
  return _argmax(a, None if axis is None else operator.index(axis), keepdims=bool(keepdims))
