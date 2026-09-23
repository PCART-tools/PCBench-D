@functools.partial(jnp.vectorize, signature='(n)->(n)')
def _normalize_quaternion(quat: jax.Array) -> jax.Array:
  return quat / _vector_norm(quat)
