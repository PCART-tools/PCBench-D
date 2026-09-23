def poisson(key: KeyArrayLike,
            lam: RealArray,
            shape: Shape | None = None,
            dtype: DTypeLikeInt = int) -> Array:
  r"""Sample Poisson random values with given shape and integer dtype.

  The values are distributed according to the probability mass function:

  .. math::
     f(k; \lambda) = \frac{\lambda^k e^{-\lambda}}{k!}

  Where `k` is a non-negative integer and :math:`\lambda > 0`.

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
  key, _ = _check_prng_key("poisson", key)
  dtypes.check_user_dtype_supported(dtype)
  # TODO(frostig): generalize underlying poisson implementation and
  # remove this check
  keys_dtype = typing.cast(prng.KeyTy, key.dtype)
  key_impl = keys_dtype._impl
  if key_impl is not prng.threefry_prng_impl:
    raise NotImplementedError(
        '`poisson` is only implemented for the threefry2x32 RNG, '
        f'not {key_impl}')
  dtype = dtypes.canonicalize_dtype(dtype)
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  else:
    shape = np.shape(lam)
  lam = jnp.broadcast_to(lam, shape)
  lam = lax.convert_element_type(lam, np.float32)
  return _poisson(key, lam, shape, dtype)
