def _index_in_group(axis_name, axis_index_groups):
  cur_device_id = axis_index(axis_name)
  if axis_index_groups is None:
    return cur_device_id
  # We use argsort to invert the axis_index_groups permutation
  flat_groups = np.array(axis_index_groups).flatten()
  device_id_to_idx = flat_groups.argsort() % len(axis_index_groups[0])
  return lax.squeeze(
      slicing.dynamic_slice_in_dim(device_id_to_idx, cur_device_id, 1), [0])
