@api.custom_jvp
def _polygamma(n: ArrayLike, x: ArrayLike) -> Array:
  dtype = lax.dtype(n).type
  n_plus = n + dtype(1)
  sign = dtype(1) - (n_plus % dtype(2)) * dtype(2)
  return jnp.where(n == 0, digamma(x), sign * jnp.exp(gammaln(n_plus)) * zeta(n_plus, x))
