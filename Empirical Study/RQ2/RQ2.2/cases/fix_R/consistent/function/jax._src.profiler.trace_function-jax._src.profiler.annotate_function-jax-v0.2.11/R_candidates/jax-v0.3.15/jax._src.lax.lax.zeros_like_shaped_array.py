def zeros_like_shaped_array(aval: Array) -> Array:
  assert isinstance(aval, ShapedArray)
  if aval.dtype == dtypes.float0:
    scalar_zero = np.zeros((), dtype=aval.dtype)
  else:
    scalar_zero = _convert_element_type(0, aval.dtype, aval.weak_type)
  return broadcast(scalar_zero, aval.shape)
