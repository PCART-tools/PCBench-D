def _rbg_split(key: jnp.ndarray, num: int) -> jnp.ndarray:
  return vmap(_threefry_split, (0, None), 1)(key.reshape(2, 2), num).reshape(num, 4)
