def _rbg_seed(seed: typing.Array) -> typing.Array:
  assert not seed.shape
  halfkey = threefry_seed(seed)
  return jnp.concatenate([halfkey, halfkey])
