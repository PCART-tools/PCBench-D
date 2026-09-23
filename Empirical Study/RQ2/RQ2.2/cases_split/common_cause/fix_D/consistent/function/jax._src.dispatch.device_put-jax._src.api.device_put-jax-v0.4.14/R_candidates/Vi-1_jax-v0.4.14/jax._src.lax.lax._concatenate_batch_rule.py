def _concatenate_batch_rule(batched_args, batch_dims, *, dimension):
  size = next(op.shape[bdim] for op, bdim in zip(batched_args, batch_dims)
              if bdim is not None)
  operands = [batching.moveaxis(op, bdim, 0) if bdim is not None
              else broadcast(op, (size,))
              for op, bdim in zip(batched_args, batch_dims)]
  return concatenate(operands, dimension + 1), 0
