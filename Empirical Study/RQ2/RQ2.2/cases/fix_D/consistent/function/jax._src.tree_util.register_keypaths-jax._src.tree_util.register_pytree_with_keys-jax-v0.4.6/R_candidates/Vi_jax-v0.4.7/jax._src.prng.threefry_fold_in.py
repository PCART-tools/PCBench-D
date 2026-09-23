def threefry_fold_in(key: jax.Array, data: jax.Array) -> jax.Array:
  assert not data.shape
  return _threefry_fold_in(key, jnp.uint32(data))
