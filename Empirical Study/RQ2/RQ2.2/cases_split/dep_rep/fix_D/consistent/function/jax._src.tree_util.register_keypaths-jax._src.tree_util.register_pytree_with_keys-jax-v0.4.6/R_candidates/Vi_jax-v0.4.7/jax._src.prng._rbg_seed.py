def _rbg_seed(seed: jax.Array) -> jax.Array:
  assert not seed.shape
  halfkey = threefry_seed(seed)
  return jnp.concatenate([halfkey, halfkey])
