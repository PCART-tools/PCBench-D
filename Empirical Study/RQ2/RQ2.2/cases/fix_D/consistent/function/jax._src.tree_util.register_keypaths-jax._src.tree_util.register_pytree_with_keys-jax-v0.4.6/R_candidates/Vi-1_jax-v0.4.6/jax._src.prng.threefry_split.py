def threefry_split(key: jax.Array, num: int) -> jax.Array:
  if config.jax_threefry_partitionable:
    return _threefry_split_foldlike(key, int(num))  # type: ignore
  else:
    return _threefry_split_original(key, int(num))  # type: ignore
