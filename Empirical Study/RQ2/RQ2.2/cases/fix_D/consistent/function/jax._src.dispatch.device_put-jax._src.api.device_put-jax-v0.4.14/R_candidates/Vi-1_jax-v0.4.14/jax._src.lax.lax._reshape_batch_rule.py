def _reshape_batch_rule(batched_args, batch_dims, *, new_sizes, dimensions):
  operand, = batched_args
  bdim, = batch_dims
  operand = batching.moveaxis(operand, bdim, 0)
  if dimensions is not None:
    dimensions = (0,) + tuple(np.add(1, dimensions))
  return reshape(operand, operand.shape[:1] + new_sizes, dimensions), 0
