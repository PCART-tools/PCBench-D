def _pmap_unmap_shaped_array(
    size: int, axis_name: core.AxisName, axis: int | None, aval: ShapedArray
  ) -> ShapedArray:
  named_shape = dict(aval.named_shape)
  named_shape.pop(axis_name, None)  # TODO: make this mandatory
  if axis is None: return aval.update(named_shape=named_shape)
  elif type(axis) is int:
    return ShapedArray(tuple_update(aval.shape, axis, size), aval.dtype,
                       named_shape=named_shape, weak_type=aval.weak_type)
  else: raise TypeError(axis)
