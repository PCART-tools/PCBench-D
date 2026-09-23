def _geqrf_batching_rule(batched_args, batch_dims):
  x, = batched_args
  bd, = batch_dims
  return geqrf(batching.moveaxis(x, bd, 0)), (0, 0)
