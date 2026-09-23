def _axis_size(a, axis):
  if not isinstance(axis, (tuple, list)):
    axis = (axis,)
  size = 1
  a_shape = np.shape(a)
  for a in axis:
    size *= maybe_named_axis(a, lambda i: a_shape[i], lambda name: lax.psum(1, name))
  return size
