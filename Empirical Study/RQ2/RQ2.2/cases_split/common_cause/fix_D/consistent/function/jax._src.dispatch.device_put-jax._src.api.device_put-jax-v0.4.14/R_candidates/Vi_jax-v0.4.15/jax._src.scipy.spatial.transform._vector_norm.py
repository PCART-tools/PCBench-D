@functools.partial(jnp.vectorize, signature='(n)->()')
def _vector_norm(vector: jax.Array) -> jax.Array:
  return jnp.sqrt(jnp.dot(vector, vector))
