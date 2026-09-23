def _unmap_dshaped_array(
    size: AxisSize, axis_name: AxisName, axis: int | None, aval: DShapedArray
  ) -> DShapedArray:
  if axis is None: return aval
  elif type(axis) is int:
    return DShapedArray(tuple_insert(aval.shape, axis, size), aval.dtype,
                        weak_type=aval.weak_type)
  else:
    raise TypeError(axis)
