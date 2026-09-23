def _rbg_seed(seed: int) -> jnp.ndarray:
  halfkey = threefry_seed(seed)
  return jnp.concatenate([halfkey, halfkey])
