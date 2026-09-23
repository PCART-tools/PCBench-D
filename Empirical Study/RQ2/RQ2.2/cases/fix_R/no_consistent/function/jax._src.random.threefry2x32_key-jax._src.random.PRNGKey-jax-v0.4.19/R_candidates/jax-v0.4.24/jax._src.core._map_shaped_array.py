def _map_shaped_array(
    size: int, axis: int | None, aval: ShapedArray) -> ShapedArray:
  assert axis is None or aval.shape[axis] == size
  # TODO: Extend the named shape
  if axis is None: return aval
  return ShapedArray(tuple_delete(aval.shape, axis), aval.dtype,
                     named_shape=aval.named_shape, weak_type=aval.weak_type)
