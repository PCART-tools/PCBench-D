def _tridiagonal_batching_rule(batched_args, batch_dims, *, lower):
  x, = batched_args
  bd, = batch_dims
  x = batching.moveaxis(x, bd, 0)
  return tridiagonal(x), 0
