def _svd_tpu(a, *, full_matrices, compute_uv):
  batch_dims = a.shape[:-2]

  fn = partial(lax_svd.svd, full_matrices=full_matrices, compute_uv=compute_uv)
  for _ in range(len(batch_dims)):
    fn = api.vmap(fn)

  if compute_uv:
    u, s, vh = fn(a)
    return [s, u, vh]
  else:
    s = fn(a)
    return [s]
