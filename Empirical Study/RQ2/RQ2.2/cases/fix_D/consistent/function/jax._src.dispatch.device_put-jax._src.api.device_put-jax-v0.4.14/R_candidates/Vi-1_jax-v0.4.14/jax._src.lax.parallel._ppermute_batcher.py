def _ppermute_batcher(axis_size, frame_name, _, vals_in, dims_in, axis_name, perm):
  (v,), (d,) = vals_in, dims_in
  if not isinstance(axis_name, (tuple, list)):
    axis_name = (axis_name,)
  remaining_axes = tuple(axis for axis in axis_name if axis != frame_name)
  if axis_size == 1 and remaining_axes:
    return ppermute_p.bind(v, perm=perm, axis_name=remaining_axes), d
  if remaining_axes:
    raise NotImplementedError("ppermute batcher only supports a single axis")
  assert axis_name[0] == frame_name, "ppermute batcher called with a wrong axis!"
  assert len(perm) == axis_size, "Permutation doesn't match the axis size!"
  if d is batching.not_mapped:
    return v, d
  perm_indices = np.zeros(axis_size, dtype=int)
  for src, dst in perm:
    perm_indices[dst] = src
  return lax_numpy.take(v, perm_indices, d), d
