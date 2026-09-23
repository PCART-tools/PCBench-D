def _insert_aval_axes(aval, axes: AxisNamePos, local_axis_sizes):
  assert isinstance(aval, core.ShapedArray)
  shape = list(aval.shape)
  named_shape = dict(aval.named_shape)
  for name, dim in sorted(axes.items(), key=lambda x: x[1]):
    shape.insert(dim, local_axis_sizes[name])
    named_shape.pop(name, None)  # The name might be missing --- it's a broadcast.
  return aval.update(shape=tuple(shape), named_shape=named_shape)
