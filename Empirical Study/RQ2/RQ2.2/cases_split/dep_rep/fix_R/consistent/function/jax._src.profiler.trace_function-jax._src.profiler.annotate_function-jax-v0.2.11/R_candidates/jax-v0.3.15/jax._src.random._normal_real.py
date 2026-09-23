@partial(jit, static_argnums=(1, 2), inline=True)
def _normal_real(key, shape, dtype) -> jnp.ndarray:
  _check_shape("normal", shape)
  lo = np.nextafter(np.array(-1., dtype), np.array(0., dtype), dtype=dtype)
  hi = np.array(1., dtype)
  u = uniform(key, shape, dtype, lo, hi)  # type: ignore[arg-type]
  return np.array(np.sqrt(2), dtype) * lax.erf_inv(u)
