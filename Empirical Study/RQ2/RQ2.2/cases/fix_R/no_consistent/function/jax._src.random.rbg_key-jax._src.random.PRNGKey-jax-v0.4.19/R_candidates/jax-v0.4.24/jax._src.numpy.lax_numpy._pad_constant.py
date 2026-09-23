def _pad_constant(array: Array, pad_width: PadValue[int], constant_values: Array) -> Array:
  nd = ndim(array)
  constant_values = broadcast_to(constant_values, (nd, 2))
  constant_values = lax_internal._convert_element_type(
      constant_values, array.dtype, dtypes.is_weakly_typed(array))
  for i in range(nd):
    widths = [(0, 0, 0)] * nd
    widths[i] = (pad_width[i][0], 0, 0)
    array = lax.pad(array, constant_values[i, 0], widths)
    widths[i] = (0, pad_width[i][1], 0)
    array = lax.pad(array, constant_values[i, 1], widths)
  return array
