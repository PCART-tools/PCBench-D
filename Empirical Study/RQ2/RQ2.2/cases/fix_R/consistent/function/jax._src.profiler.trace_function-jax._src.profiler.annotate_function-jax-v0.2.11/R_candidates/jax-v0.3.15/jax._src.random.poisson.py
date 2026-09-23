def poisson(key: KeyArray,
            lam: RealArray,
            shape: Optional[Sequence[int]] = None,
            dtype: DTypeLikeInt = dtypes.int_) -> jnp.ndarray:
  """Sample Poisson random values with given shape and integer dtype.

  Args:
    key: a PRNG key used as the random key.
    lam: rate parameter (mean of the distribution), must be >= 0. Must be broadcast-compatible with ``shape``
    shape: optional, a tuple of nonnegative integers representing the result
      shape. Default (None) produces a result shape equal to ``lam.shape``.
    dtype: optional, a integer dtype for the returned values (default int64 if
      jax_enable_x64 is true, otherwise int32).

  Returns:
    A random array with the specified dtype and with shape given by ``shape`` if
    ``shape is not None, or else by ``lam.shape``.
  """
  key, _ = _check_prng_key(key)
  if key.impl is not prng.threefry_prng_impl:
    raise NotImplementedError(
        '`poisson` is only implemented for the threefry2x32 RNG, '
        f'not {key.impl}')
  dtype = dtypes.canonicalize_dtype(dtype)
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  else:
    shape = np.shape(lam)
  lam = jnp.broadcast_to(lam, shape)
  lam = lax.convert_element_type(lam, np.float32)
  return _poisson(key, lam, shape, dtype)
