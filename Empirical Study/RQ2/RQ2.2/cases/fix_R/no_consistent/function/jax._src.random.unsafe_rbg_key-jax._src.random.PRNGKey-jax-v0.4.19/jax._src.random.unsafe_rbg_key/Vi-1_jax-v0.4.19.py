def unsafe_rbg_key(seed: int) -> KeyArray:
  """Creates an unsafe RBG PRNG key from an integer seed."""
  impl = prng.unsafe_rbg_prng_impl
  _check_default_impl_with_no_custom_prng(impl, 'unsafe_rbg')
  key = prng.random_seed(seed, impl=impl)
  return _return_prng_keys(True, key)
