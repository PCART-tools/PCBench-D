def _rbg_split(key: jax.Array, num: int) -> jax.Array:
  if config.jax_threefry_partitionable:
    _threefry_split = _threefry_split_foldlike
  else:
    _threefry_split = _threefry_split_original
  return vmap(
      _threefry_split, (0, None), 1)(key.reshape(2, 2), num).reshape(num, 4)
