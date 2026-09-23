def _reduction_dims(a, axis):
  if axis is None:
    return (tuple(range(np.ndim(a))),) * 2
  elif not isinstance(axis, (np.ndarray, tuple, list)):
    axis = (axis,)
  canon_axis = tuple(_canonicalize_axis_allow_named(x, np.ndim(a))
                     for x in axis)
  if len(canon_axis) != len(set(canon_axis)):
    raise ValueError(f"duplicate value in 'axis': {axis}")
  canon_pos_axis = tuple(x for x in canon_axis if isinstance(x, int))
  if len(canon_pos_axis) != len(canon_axis):
    return canon_pos_axis, canon_axis
  else:
    return canon_axis, canon_axis
