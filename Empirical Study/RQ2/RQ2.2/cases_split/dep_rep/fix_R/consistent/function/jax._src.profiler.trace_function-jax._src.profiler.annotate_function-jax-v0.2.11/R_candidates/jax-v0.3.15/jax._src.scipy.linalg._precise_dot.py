def _precise_dot(A, B):
  return jnp.dot(A, B, precision=lax.Precision.HIGHEST)
