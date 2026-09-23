def _eval_expint_k(A, B, x):
  # helper function for all subsequent intervals
  A, B = (jnp.array(U, dtype=x.dtype) for U in [A, B])
  one = _lax_const(x, 1.0)
  w = one / x
  f = jnp.polyval(A, w) / jnp.polyval(B, w)
  f = w * f + one
  return jnp.exp(x) * w * f
