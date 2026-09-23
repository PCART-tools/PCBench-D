def zeros_like_shaped_array(aval: ShapedArray) -> Array:
  assert isinstance(aval, ShapedArray)
  if dtypes.issubdtype(aval.dtype, dtypes.extended):
    scalar_zero = aval.dtype._rules.zero(aval.dtype)
  elif aval.dtype == dtypes.float0:
    scalar_zero = np.zeros((), dtype=aval.dtype)
  else:
    scalar_zero = _convert_element_type(0, aval.dtype, aval.weak_type)
  return broadcast(scalar_zero, aval.shape)
