def _check_prng_key(name: str, key: KeyArrayLike, *,
                    allow_batched: bool = False,
                    error_on_batched: bool = False) -> tuple[KeyArray, bool]:
  if isinstance(key, Array) and dtypes.issubdtype(key.dtype, dtypes.prng_key):
    wrapped_key = key
    wrapped = False
  elif _arraylike(key):
    # Call random_wrap here to surface errors for invalid keys.
    wrapped_key = prng.random_wrap(key, impl=default_prng_impl())
    wrapped = True
    if config.legacy_prng_key.value == 'error':
      raise ValueError(
        'Legacy uint32 key array passed as key to jax.random function. '
        'Please create keys using jax.random.key(). If use of a raw key array '
        'was intended, set jax_legacy_prng_key="allow".')
    elif config.legacy_prng_key.value == 'warn':
      warnings.warn(
        'Legacy uint32 key array passed as key to jax.random function. '
        'Please create keys using jax.random.key(). If use of a raw key array '
        'was intended, set jax_legacy_prng_key="allow".', stacklevel=2)
    elif config.enable_custom_prng.value:
      # TODO(jakevdp): possibly remove this warning condition.
      warnings.warn(
          'Raw arrays as random keys to jax.random functions are deprecated. '
          'Assuming valid threefry2x32 key for now.',
          FutureWarning)
  else:
    raise TypeError(f'unexpected PRNG key type {type(key)}')

  if (not allow_batched) and wrapped_key.ndim:
    msg = (f"{name} accepts a single key, but was given a key array of "
           f"shape {np.shape(key)} != (). Use jax.vmap for batching.")
    if error_on_batched:
      raise ValueError(msg)
    else:
      warnings.warn(msg + " In a future JAX version, this will be an error.",
                    FutureWarning, stacklevel=3)

  return wrapped_key, wrapped
