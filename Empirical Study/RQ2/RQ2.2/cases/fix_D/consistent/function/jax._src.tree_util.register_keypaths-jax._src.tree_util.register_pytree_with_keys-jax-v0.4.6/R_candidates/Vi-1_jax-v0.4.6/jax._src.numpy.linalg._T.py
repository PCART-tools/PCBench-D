def _T(x: ArrayLike) -> Array:
  return jnp.swapaxes(x, -1, -2)
