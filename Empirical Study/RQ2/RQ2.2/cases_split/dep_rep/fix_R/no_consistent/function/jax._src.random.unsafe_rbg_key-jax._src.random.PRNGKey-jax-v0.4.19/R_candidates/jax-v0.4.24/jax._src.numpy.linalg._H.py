def _H(x: ArrayLike) -> Array:
  return ufuncs.conjugate(jnp.matrix_transpose(x))
