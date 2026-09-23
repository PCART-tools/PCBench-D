@functools.partial(jnp.vectorize, signature='(m,m),(m),()->(m)')
def _apply(matrix: jax.Array, vector: jax.Array, inverse: bool) -> jax.Array:
  return jnp.where(inverse, matrix.T, matrix) @ vector
