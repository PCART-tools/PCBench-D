@implements(np.average)
def average(a: ArrayLike, axis: Axis = None, weights: ArrayLike | None = None,
            returned: bool = False, keepdims: bool = False) -> Array | tuple[Array, Array]:
  return _average(a, _ensure_optional_axes(axis), weights, returned, keepdims)
