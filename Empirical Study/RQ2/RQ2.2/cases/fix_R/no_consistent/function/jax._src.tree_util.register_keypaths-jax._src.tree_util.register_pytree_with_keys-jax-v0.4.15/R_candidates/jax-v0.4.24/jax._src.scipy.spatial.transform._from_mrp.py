@functools.partial(jnp.vectorize, signature='(m)->(n)')
def _from_mrp(mrp: jax.Array) -> jax.Array:
  mrp_squared_plus_1 = jnp.dot(mrp, mrp) + 1
  return jnp.hstack([2 * mrp[:3], (2 - mrp_squared_plus_1)]) / mrp_squared_plus_1
