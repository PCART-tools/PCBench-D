@_wraps(np.average)
def average(a: ArrayLike, axis: Axis = None, weights: Optional[ArrayLike] = None,
            returned: bool = False, keepdims: bool = False) -> Union[Array, tuple[Array, Array]]:
  return _average(a, _ensure_optional_axes(axis), weights, returned, keepdims)
