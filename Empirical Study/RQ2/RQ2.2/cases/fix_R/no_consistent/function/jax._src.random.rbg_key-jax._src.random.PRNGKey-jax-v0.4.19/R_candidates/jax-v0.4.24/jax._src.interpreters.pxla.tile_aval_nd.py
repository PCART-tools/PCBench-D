def tile_aval_nd(axis_sizes, in_axes: ArrayMapping, aval):
  assert isinstance(aval, ShapedArray)
  shape = list(aval.shape)
  named_shape = dict(aval.named_shape)
  for name, axis in in_axes.items():
    assert shape[axis] % axis_sizes[name] == 0
    assert name not in named_shape
    named_shape[name] = axis_sizes[name]
    shape[axis] //= axis_sizes[name]
  return aval.update(shape=tuple(shape), named_shape=named_shape)
