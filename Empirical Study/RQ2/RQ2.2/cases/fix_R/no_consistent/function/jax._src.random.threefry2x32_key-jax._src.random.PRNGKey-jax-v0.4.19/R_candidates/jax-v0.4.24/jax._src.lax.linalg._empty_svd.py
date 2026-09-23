def _empty_svd(a, *, full_matrices, compute_uv):
  batch_shape = a.shape[:-2]
  m, n = a.shape[-2:]
  s = jnp.empty(batch_shape + (0,), dtype=lax_internal._complex_basetype(a.dtype))
  if not compute_uv:
    return (s,)
  if full_matrices:
    size = max(m, n)
    u = jnp.broadcast_to(jnp.eye(size, dtype=a.dtype), batch_shape + (size, size))
  else:
    u = jnp.empty(batch_shape + (m, n), dtype=a.dtype)
  v = jnp.empty(batch_shape + (0, 0), dtype=a.dtype)
  if m < n:
    u, v = v, u
  return s, u, v
