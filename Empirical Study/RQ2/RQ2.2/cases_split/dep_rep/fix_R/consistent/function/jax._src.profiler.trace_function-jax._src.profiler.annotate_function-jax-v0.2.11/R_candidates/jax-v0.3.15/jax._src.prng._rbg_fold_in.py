def _rbg_fold_in(key: jnp.ndarray, data: int) -> jnp.ndarray:
  return vmap(_threefry_fold_in, (0, None), 0)(key.reshape(2, 2), data).reshape(4)
