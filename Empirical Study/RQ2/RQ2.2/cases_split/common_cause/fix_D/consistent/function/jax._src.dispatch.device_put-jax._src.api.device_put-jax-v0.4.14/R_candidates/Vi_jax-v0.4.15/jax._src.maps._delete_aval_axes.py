def _delete_aval_axes(aval, axes: AxisNamePos, global_axis_sizes):
  assert isinstance(aval, core.ShapedArray)
  shape = list(aval.shape)
  named_shape = dict(aval.named_shape)
  for name, dim in sorted(axes.items(), key=lambda x: x[1], reverse=True):
    named_shape[name] = global_axis_sizes[name]
    del shape[dim]
  return aval.update(shape=tuple(shape), named_shape=named_shape)
