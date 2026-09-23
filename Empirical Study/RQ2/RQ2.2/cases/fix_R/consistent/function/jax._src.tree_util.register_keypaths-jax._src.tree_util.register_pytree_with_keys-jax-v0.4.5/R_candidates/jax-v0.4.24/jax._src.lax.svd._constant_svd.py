@functools.partial(jax.jit, static_argnums=(2, 3))
def _constant_svd(
    a: Any, return_nan: bool, full_matrices: bool, compute_uv: bool = True
) -> Any | Sequence[Any]:
  """SVD on matrix of all zeros."""
  m, n = a.shape
  k = min(m, n)
  s = jnp.where(
      return_nan,
      jnp.full(shape=(k,), fill_value=jnp.nan, dtype=a.real.dtype),
      jnp.zeros(shape=(k,), dtype=a.real.dtype),
  )
  if compute_uv:
    fill_value = (
        jnp.nan + 1j * jnp.nan
        if jnp.issubdtype(a.dtype, jnp.complexfloating)
        else jnp.nan
    )
    if full_matrices:
      u = jnp.where(
          return_nan,
          jnp.full((m, m), fill_value, dtype=a.dtype),
          jnp.eye(m, m, dtype=a.dtype),
      )
      vh = jnp.where(
          return_nan,
          jnp.full((n, n), fill_value, dtype=a.dtype),
          jnp.eye(n, n, dtype=a.dtype),
      )
    else:
      u = jnp.where(
          return_nan,
          jnp.full((m, k), fill_value, dtype=a.dtype),
          jnp.eye(m, k, dtype=a.dtype),
      )
      vh = jnp.where(
          return_nan,
          jnp.full((k, n), fill_value, dtype=a.dtype),
          jnp.eye(k, n, dtype=a.dtype),
      )
    return (u, s, vh)
  else:
    return s
