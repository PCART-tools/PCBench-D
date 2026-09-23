def _all_to_all_via_all_gather(x, *, axis_name, split_axis, concat_axis, axis_index_groups):
  idx = _index_in_group(axis_name, axis_index_groups)
  full = all_gather(x, axis_name, axis_index_groups=axis_index_groups)
  axis_size = full.shape[0]
  tile_size = x.shape[split_axis] // axis_size
  tile_base_idx = idx * tile_size
  sliced = slicing.dynamic_slice_in_dim(full, tile_base_idx, tile_size,
                                        split_axis + 1)
  return _foldaxis(concat_axis, _moveaxis(0, concat_axis, sliced))
