def threefry_fold_in(key: jnp.ndarray, data: int) -> jnp.ndarray:
  return _threefry_fold_in(key, jnp.uint32(data))
