@functools.partial(jnp.vectorize, signature='(n)->()')
def _magnitude(quat: jax.Array) -> jax.Array:
  return 2. * jnp.arctan2(_vector_norm(quat[:3]), jnp.abs(quat[3]))
