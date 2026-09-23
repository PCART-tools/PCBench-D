def threefry_2x32(keypair, count):
  warnings.warn('jax.random.threefry_2x32 has moved to jax.prng.threefry_2x32 '
                'and will be removed from `random` module.', FutureWarning)
  return prng.threefry_2x32(keypair, count)
