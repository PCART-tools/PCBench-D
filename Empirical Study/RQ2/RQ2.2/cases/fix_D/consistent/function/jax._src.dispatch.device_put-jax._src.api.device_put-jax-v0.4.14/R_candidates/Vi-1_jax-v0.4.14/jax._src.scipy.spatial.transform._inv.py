@functools.partial(jnp.vectorize, signature='(n)->(n)')
def _inv(quat: jax.Array) -> jax.Array:
  return quat.at[3].set(-quat[3])
