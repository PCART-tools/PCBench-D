def _squeeze_batch_rule(batched_args, batch_dims, *, dimensions):
  operand, = batched_args
  bdim, = batch_dims
  operand, bdim = batching.move_stacked_axis(operand, bdim, 0)
  dimensions = tuple(np.add(1, dimensions))
  out_stack_dim = bdim.stacked_axis if isinstance(bdim, RaggedAxis) else bdim
  bdim_out = batching.shape_as_bdim(
      out_stack_dim,
      _compute_squeeze_shape(batching.bdim_as_shape(bdim, operand.shape), dimensions))
  return squeeze(operand, dimensions=dimensions), bdim_out
