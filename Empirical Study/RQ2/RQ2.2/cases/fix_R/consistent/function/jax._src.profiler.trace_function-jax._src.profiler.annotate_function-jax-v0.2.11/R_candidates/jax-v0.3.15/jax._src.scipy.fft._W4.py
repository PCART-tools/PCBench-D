def _W4(N, k):
  N, k = _promote_dtypes_complex(N, k)
  return jnp.exp(-.5j * jnp.pi * k / N)
