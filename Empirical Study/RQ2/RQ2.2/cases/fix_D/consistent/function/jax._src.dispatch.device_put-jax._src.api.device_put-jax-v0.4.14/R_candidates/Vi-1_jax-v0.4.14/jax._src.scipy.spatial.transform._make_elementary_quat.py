@functools.partial(jnp.vectorize, signature='(),()->(n)')
def _make_elementary_quat(axis: int, angle: jax.Array) -> jax.Array:
  quat = jnp.zeros(4, dtype=angle.dtype)
  quat = quat.at[3].set(jnp.cos(angle / 2.))
  quat = quat.at[axis].set(jnp.sin(angle / 2.))
  return quat
