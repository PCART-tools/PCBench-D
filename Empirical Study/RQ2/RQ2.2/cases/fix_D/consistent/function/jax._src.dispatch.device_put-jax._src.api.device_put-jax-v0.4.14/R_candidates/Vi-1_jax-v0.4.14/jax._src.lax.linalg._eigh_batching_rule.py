def _eigh_batching_rule(batched_args, batch_dims, *, lower, sort_eigenvalues):
  x, = batched_args
  bd, = batch_dims
  x = batching.moveaxis(x, bd, 0)
  return eigh_p.bind(x, lower=lower, sort_eigenvalues=sort_eigenvalues), (0, 0)
