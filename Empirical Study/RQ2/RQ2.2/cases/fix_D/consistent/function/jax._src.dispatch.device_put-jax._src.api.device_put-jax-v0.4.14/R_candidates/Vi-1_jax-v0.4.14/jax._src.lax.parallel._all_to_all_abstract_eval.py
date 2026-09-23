def _all_to_all_abstract_eval(x, axis_name, split_axis, concat_axis, axis_index_groups):
  input_aval = raise_to_shaped(x)
  shape = list(input_aval.shape)
  axis_size = psum(1, axis_name) if axis_index_groups is None else len(axis_index_groups[0])
  assert shape[split_axis] % axis_size == 0, (shape[split_axis], axis_size)
  shape[split_axis] //= axis_size
  shape[concat_axis] *= axis_size
  return input_aval.update(shape=tuple(shape), weak_type=False)
