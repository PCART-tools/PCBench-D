@functools.partial(jax.jit, static_argnums=(1, 2))
def _zero_svd(a: Any,
              full_matrices: bool,
              compute_uv: bool = True) -> Union[Any, Sequence[Any]]:
  """SVD on matrix of all zeros."""
  m, n = a.shape
  k = min(m, n)
  s = jnp.zeros(shape=(k,), dtype=a.real.dtype)
  if compute_uv:
    if full_matrices:
      u = jnp.eye(m, m, dtype=a.dtype)
      vh = jnp.eye(n, n, dtype=a.dtype)
    else:
      u = jnp.eye(m, k, dtype=a.dtype)
      vh = jnp.eye(k, n, dtype=a.dtype)
    return (u, s, vh)
  else:
    return s
