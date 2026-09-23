@_wraps(np.average)
def average(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, weights=None,
            returned=False, keepdims=False):
  return _average(a, _ensure_optional_axes(axis), weights, returned, keepdims)
