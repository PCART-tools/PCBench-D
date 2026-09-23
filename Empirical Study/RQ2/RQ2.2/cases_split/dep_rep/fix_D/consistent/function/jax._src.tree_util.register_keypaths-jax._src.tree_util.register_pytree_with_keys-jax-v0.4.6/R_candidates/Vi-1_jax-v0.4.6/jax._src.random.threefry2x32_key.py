def threefry2x32_key(seed: int) -> KeyArray:
  """Creates a threefry2x32 PRNG key from an integer seed."""
  impl = prng.threefry_prng_impl
  _check_default_impl_with_no_custom_prng(impl, 'threefry2x32')
  key = prng.seed_with_impl(impl, seed)
  return _return_prng_keys(True, key)
