def _allreduce_impl(pos_reducer, *args, axes, axis_index_groups):
  assert axis_index_groups is None
  assert all(isinstance(axis, int) for axis in axes)
  return [pos_reducer(arg, axes) for arg in args]
