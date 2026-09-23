def rademacher(key: KeyArray,
               shape: Sequence[int],
               dtype: DTypeLikeInt = dtypes.int_) -> jnp.ndarray:
  """Sample from a Rademacher distribution.

  Args:
    key: a PRNG key.
    shape: The shape of the returned samples.
    dtype: The type used for samples.

  Returns:
    A jnp.array of samples, of shape `shape`. Each element in the output has
    a 50% change of being 1 or -1.

  """
  key, _ = _check_prng_key(key)
  dtype = dtypes.canonicalize_dtype(dtype)
  shape = core.canonicalize_shape(shape)
  return _rademacher(key, shape, dtype)
