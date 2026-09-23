def _qr_lowering(a, *, full_matrices):
  *batch_dims, m, n = a.shape
  if m == 0 or n == 0:
    k = m if full_matrices else min(m, n)
    q = jnp.broadcast_to(jnp.eye(m, k, dtype=a.dtype), (*batch_dims, m, k))
    r = jnp.empty((*batch_dims, k, n), dtype=a.dtype)
    return q, r

  r, taus = geqrf(a)
  if m < n:
    q = householder_product(r[..., :m, :m], taus)
  elif full_matrices:
    pads = [(0, 0, 0)] * (len(batch_dims) + 1) + [(0, m - n, 0)]
    q = lax.pad(r, lax_internal._zero(r), pads)
    q = householder_product(q, taus)
  else:
    q = householder_product(r, taus)
    r = r[..., :n, :n]
  r = jnp.triu(r)
  return q, r
