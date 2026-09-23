def _H(x):
  return jnp.conjugate(jnp.swapaxes(x, -1, -2))
