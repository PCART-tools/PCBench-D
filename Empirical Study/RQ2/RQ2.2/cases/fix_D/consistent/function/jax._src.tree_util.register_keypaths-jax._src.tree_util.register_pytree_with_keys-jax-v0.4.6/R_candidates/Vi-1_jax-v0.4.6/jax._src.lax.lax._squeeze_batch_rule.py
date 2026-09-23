def _squeeze_batch_rule(batched_args, batch_dims, *, dimensions):
  operand, = batched_args
  bdim, = batch_dims
  operand = batching.moveaxis(operand, bdim, 0)
  dimensions = tuple(np.add(1, dimensions))
  return squeeze(operand, dimensions=dimensions), 0
