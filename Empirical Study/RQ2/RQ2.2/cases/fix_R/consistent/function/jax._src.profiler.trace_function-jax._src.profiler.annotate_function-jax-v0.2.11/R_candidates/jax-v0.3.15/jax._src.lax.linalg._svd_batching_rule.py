def _svd_batching_rule(batched_args, batch_dims, *, full_matrices, compute_uv):
  x, = batched_args
  bd, = batch_dims
  x = batching.moveaxis(x, bd, 0)
  outs = svd_p.bind(x, full_matrices=full_matrices, compute_uv=compute_uv)

  if compute_uv:
    return outs, (0, 0, 0)
  else:
    return outs, (0,)
