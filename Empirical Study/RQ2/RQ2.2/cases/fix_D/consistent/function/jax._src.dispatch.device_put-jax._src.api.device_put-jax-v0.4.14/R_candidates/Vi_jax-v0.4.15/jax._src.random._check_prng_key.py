def _check_prng_key(key) -> tuple[prng.PRNGKeyArray, bool]:
  # TODO(frostig): remove once we always enable_custom_prng
  if isinstance(key, prng.PRNGKeyArray):
    return key, False
  elif _arraylike(key):
    # Call random_wrap here to surface errors for invalid keys.
    wrapped_key = prng.random_wrap(key, impl=default_prng_impl())
    if config.jax_legacy_prng_key == 'error':
      raise ValueError(
        'Legacy uint32 key array passed as key to jax.random function. '
        'Please create keys using jax.random.key(). If use of a raw key array '
        'was intended, set jax_legacy_prng_key="allow".')
    elif config.jax_legacy_prng_key == 'warn':
      warnings.warn(
        'Legacy uint32 key array passed as key to jax.random function. '
        'Please create keys using jax.random.key(). If use of a raw key array '
        'was intended, set jax_legacy_prng_key="allow".', stacklevel=2)
    elif config.jax_enable_custom_prng:
      # TODO(jakevdp): possibly remove this warning condition.
      warnings.warn(
          'Raw arrays as random keys to jax.random functions are deprecated. '
          'Assuming valid threefry2x32 key for now.',
          FutureWarning)
    return wrapped_key, True
  else:
    raise TypeError(f'unexpected PRNG key type {type(key)}')
