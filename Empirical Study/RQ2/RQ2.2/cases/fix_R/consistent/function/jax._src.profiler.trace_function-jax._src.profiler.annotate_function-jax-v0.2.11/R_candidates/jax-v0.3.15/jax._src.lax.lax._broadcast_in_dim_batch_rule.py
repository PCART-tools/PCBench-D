def _broadcast_in_dim_batch_rule(batched_args, batch_dims, *, shape,
                                 broadcast_dimensions):
  operand, = batched_args
  bdim, = batch_dims
  new_operand = batching.moveaxis(operand, bdim, 0)
  new_shape = (operand.shape[bdim],) + shape
  new_broadcast_dimensions = (0,) + tuple(np.add(1, broadcast_dimensions))
  return broadcast_in_dim(new_operand, new_shape, new_broadcast_dimensions), 0
