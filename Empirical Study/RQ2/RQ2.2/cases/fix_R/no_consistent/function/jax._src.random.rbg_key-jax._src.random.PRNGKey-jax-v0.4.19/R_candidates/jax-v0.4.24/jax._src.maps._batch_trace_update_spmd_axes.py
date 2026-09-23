def _batch_trace_update_spmd_axes(
    spmd_in_axes, spmd_out_axes_thunk,
    axis_name, dims, dims_out_thunk):
  """Extends spmd in and out axes with the position of the trace's batch dimension."""
  not_mapped = batching.not_mapped
  def insert_spmd_axis(axes, nd):
    too_short = nd - len(axes)
    if too_short > 0:
      axes += (None,) * too_short
    return tuple_insert(axes, nd, axis_name)

  if spmd_in_axes is None:
    spmd_in_axes = ((),) * len(dims)
  new_spmd_in_axes = tuple(
    spmd_axes if d is not_mapped else insert_spmd_axis(spmd_axes, d)
    for spmd_axes, d in zip(spmd_in_axes, dims))

  @as_hashable_function(closure=spmd_out_axes_thunk)
  def new_spmd_out_axes_thunk():
    dims_out = dims_out_thunk()
    if spmd_out_axes_thunk is None:
      spmd_out_axes = ((),) * len(dims_out)
    else:
      spmd_out_axes = spmd_out_axes_thunk()
    return tuple(
      spmd_out_axes if nd is not_mapped else insert_spmd_axis(spmd_out_axes, nd)
      for spmd_out_axes, nd in zip(spmd_out_axes, dims_out))

  return new_spmd_in_axes, new_spmd_out_axes_thunk
