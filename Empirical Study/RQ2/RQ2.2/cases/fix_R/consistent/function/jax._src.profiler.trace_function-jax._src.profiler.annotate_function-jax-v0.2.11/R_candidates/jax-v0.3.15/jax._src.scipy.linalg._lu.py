@partial(jit, static_argnums=(1,))
def _lu(a, permute_l):
  a, = _promote_dtypes_inexact(jnp.asarray(a))
  lu, _, permutation = lax_linalg.lu(a)
  dtype = lax.dtype(a)
  m, n = jnp.shape(a)
  p = jnp.real(jnp.array(permutation[None, :] == jnp.arange(m, dtype=permutation.dtype)[:, None], dtype=dtype))
  k = min(m, n)
  l = jnp.tril(lu, -1)[:, :k] + jnp.eye(m, k, dtype=dtype)
  u = jnp.triu(lu)[:k, :]
  if permute_l:
    return jnp.matmul(p, l), u
  else:
    return p, l, u
