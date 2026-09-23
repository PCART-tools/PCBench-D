def _broadcast_in_dim_batch_rule(batched_args, batch_dims, shape,
                                 broadcast_dimensions):
  # `dyn_shape` is the dynamic portion of the target shape.  `shape`
  # is the target shape, with `None` for dynamic sections.
  # broadcast_dimensions gives indices where dimensions of the input
  # have to go: dimension i of the input becomes dimension
  # broadcast_dimensions[i] of the output.
  operand, *dyn_shape = batched_args
  operand_bdim, *dyn_shape_bdims = batch_dims

  stacked_size = None
  if operand_bdim is not None:
    if isinstance(operand_bdim, RaggedAxis):
      stacked_axis = operand_bdim.stacked_axis
    else:
      stacked_axis = operand_bdim
    new_operand = batching.moveaxis(operand, stacked_axis, 0)
    if isinstance(operand_bdim, RaggedAxis):
      stacked_size = operand_bdim.size
    else:
      stacked_size = operand.shape[stacked_axis]
    new_broadcast_dimensions = (0,) + tuple(np.add(1, broadcast_dimensions))
  else:
    new_operand = operand
    new_broadcast_dimensions = tuple(np.add(1, broadcast_dimensions))

  # TODO(mattjj,axch) This section assumes that the shape of the operand is
  # broadcast-compatible with the requested shape.  We should tweak vmap to run
  # the abstract_eval rule so this can be checked while the raggedness
  # information is available.
  dyn_limits = []
  out_ragged_sizes = []
  for sizes, bdim in zip(dyn_shape, dyn_shape_bdims):
    if bdim is None:
      # TODO(mattjj,axch) Is this what bdim == None means?
      assert isinstance(sizes, int)
      bound = sizes
    else:
      bound = sizes.dtype.bound
      out_ragged_sizes.append(sizes)
      if stacked_size is None:
        stacked_size = len(sizes)
      else:
        msg = "All segments lengths arrays must be the same length"
        assert len(sizes) == stacked_size, msg
    dyn_limits.append(bound)
  new_shape = (stacked_size,) + _merge_dyn_shape(shape, dyn_limits)
  result = broadcast_in_dim(new_operand, new_shape, new_broadcast_dimensions)
  out_ragged_axes = [idx+1 for idx, s in enumerate(shape) if s is None]
  out_bdim = batching.make_batch_axis(
      result.ndim, 0, zip(out_ragged_axes, out_ragged_sizes))
  return result, out_bdim
