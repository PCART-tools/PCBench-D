def wrap_key_data(key_bits_array: Array, *,
                  impl: PRNGSpecDesc | None = None):
  """Wrap an array of key data bits into a PRNG key array.

  Args:
    key_bits_array: a ``uint32`` array with trailing shape corresponding to
      the key shape of the PRNG implementation specified by ``impl``.
    impl: optional, specifies a PRNG implementation, as in ``random.key``.

  Returns:
    A PRNG key array, whose dtype is a subdtype of ``jax.dtypes.prng_key``
      corresponding to ``impl``, and whose shape equals the leading shape
      of ``key_bits_array.shape`` up to the key bit dimensions.
  """
  impl_obj = resolve_prng_impl(impl)
  return prng.random_wrap(key_bits_array, impl=impl_obj)
