def rbg_key(seed: int | ArrayLike) -> KeyArray:
  """Creates an RBG PRNG key from an integer seed."""
  impl = prng.rbg_prng_impl
  _check_default_impl_with_no_custom_prng(impl, 'rbg')
  key = prng.random_seed(seed, impl=impl)
  return _return_prng_keys(True, key)
