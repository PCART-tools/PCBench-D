def _H(x: ArrayLike) -> Array:
  return ufuncs.conjugate(jnp.swapaxes(x, -1, -2))
