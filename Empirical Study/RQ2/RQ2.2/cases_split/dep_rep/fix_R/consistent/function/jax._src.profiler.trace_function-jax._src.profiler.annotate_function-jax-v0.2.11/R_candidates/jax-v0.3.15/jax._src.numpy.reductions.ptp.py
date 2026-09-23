@_wraps(np.ptp, skip_params=['out'])
def ptp(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
        keepdims=False):
  return _ptp(a, _ensure_optional_axes(axis), out, keepdims)
