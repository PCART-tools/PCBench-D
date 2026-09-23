@implements(np.ptp, skip_params=['out'])
def ptp(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False) -> Array:
  return _ptp(a, _ensure_optional_axes(axis), out, keepdims)
