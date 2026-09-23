def _cast_to_shaped_array(aval: core.AbstractValue) -> ShapedArray:
  assert isinstance(aval, ShapedArray), aval
  return cast(ShapedArray, aval)
