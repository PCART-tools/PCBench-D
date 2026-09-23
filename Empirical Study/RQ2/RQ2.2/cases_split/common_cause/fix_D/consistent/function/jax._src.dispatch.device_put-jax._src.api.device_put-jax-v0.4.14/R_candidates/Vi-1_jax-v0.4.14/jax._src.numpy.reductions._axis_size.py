def _axis_size(a: ArrayLike, axis: Union[int, Sequence[int]]):
  if not isinstance(axis, (tuple, list)):
    axis_seq: Sequence[int] = (axis,)  # type: ignore[assignment]
  else:
    axis_seq = axis
  size = 1
  a_shape = np.shape(a)
  for a in axis_seq:
    size *= maybe_named_axis(a, lambda i: a_shape[i], lambda name: lax.psum(1, name))
  return size
