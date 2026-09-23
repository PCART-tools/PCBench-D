def wrap_key_data(key_bits_array: Array, *, impl: Optional[str] = None):
  impl_obj = random.resolve_prng_impl(impl)
  return prng.random_wrap(key_bits_array, impl=impl_obj)
