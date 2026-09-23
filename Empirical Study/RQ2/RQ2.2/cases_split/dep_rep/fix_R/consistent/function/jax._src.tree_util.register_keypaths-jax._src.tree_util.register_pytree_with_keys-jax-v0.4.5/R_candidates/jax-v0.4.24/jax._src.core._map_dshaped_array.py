def _map_dshaped_array(
    size: AxisSize, axis: int | None, aval: DShapedArray) -> DShapedArray:
  if axis is None: return aval
  return DShapedArray(tuple_delete(aval.shape, axis), aval.dtype,
                      aval.weak_type)
