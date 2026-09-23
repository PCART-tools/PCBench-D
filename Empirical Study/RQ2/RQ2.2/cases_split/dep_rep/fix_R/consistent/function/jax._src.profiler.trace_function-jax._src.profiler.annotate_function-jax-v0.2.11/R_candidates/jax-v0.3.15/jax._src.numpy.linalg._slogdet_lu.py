@custom_jvp
def _slogdet_lu(a):
  dtype = lax.dtype(a)
  lu, pivot, _ = lax_linalg.lu(a)
  diag = jnp.diagonal(lu, axis1=-2, axis2=-1)
  is_zero = jnp.any(diag == jnp.array(0, dtype=dtype), axis=-1)
  iota = lax.expand_dims(jnp.arange(a.shape[-1], dtype=pivot.dtype),
                         range(pivot.ndim - 1))
  parity = jnp.count_nonzero(pivot != iota, axis=-1)
  if jnp.iscomplexobj(a):
    sign = jnp.prod(diag / jnp.abs(diag).astype(diag.dtype), axis=-1)
  else:
    sign = jnp.array(1, dtype=dtype)
    parity = parity + jnp.count_nonzero(diag < 0, axis=-1)
  sign = jnp.where(is_zero,
                  jnp.array(0, dtype=dtype),
                  sign * jnp.array(-2 * (parity % 2) + 1, dtype=dtype))
  logdet = jnp.where(
      is_zero, jnp.array(-jnp.inf, dtype=dtype),
      jnp.sum(jnp.log(jnp.abs(diag)).astype(dtype), axis=-1))
  return sign, jnp.real(logdet)
