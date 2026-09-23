def _eval_expint_k(A: List[float], B: List[float], x: Array) -> Array:
  # helper function for all subsequent intervals
  A_arr = jnp.array(A, dtype=x.dtype)
  B_arr = jnp.array(B, dtype=x.dtype)
  one = _lax_const(x, 1.0)
  w = one / x
  f = jnp.polyval(A_arr, w) / jnp.polyval(B_arr, w)
  f = w * f + one
  return jnp.exp(x) * w * f
