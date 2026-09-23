def _qr_batching_rule(batched_args, batch_dims, *, full_matrices):
  x, = batched_args
  bd, = batch_dims
  x = batching.moveaxis(x, bd, 0)
  return qr_p.bind(x, full_matrices=full_matrices), (0, 0)
