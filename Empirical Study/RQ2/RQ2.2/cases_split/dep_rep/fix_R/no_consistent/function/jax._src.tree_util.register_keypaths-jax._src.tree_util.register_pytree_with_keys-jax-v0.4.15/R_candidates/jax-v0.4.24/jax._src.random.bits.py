def bits(key: KeyArrayLike,
         shape: Shape = (),
         dtype: DTypeLikeUInt | None = None) -> Array:
  """Sample uniform bits in the form of unsigned integers.

  Args:
    key: a PRNG key used as the random key.
    shape: optional, a tuple of nonnegative integers representing the result
      shape. Default ``()``.
    dtype: optional, an unsigned integer dtype for the returned values (default
      ``uint64`` if ``jax_enable_x64`` is true, otherwise ``uint32``).

  Returns:
    A random array with the specified shape and dtype.
  """
  key, _ = _check_prng_key("bits", key)
  if dtype is None:
    dtype = dtypes.canonicalize_dtype(jnp.uint)
  else:
    dtypes.check_user_dtype_supported(dtype)
  if not dtypes.issubdtype(dtype, np.unsignedinteger):
    raise ValueError("dtype argument to `bits` must be an unsigned int dtype, "
                     f"got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  shape = core.canonicalize_shape(shape)
  bit_width = dtype.itemsize * 8
  return _random_bits(key, bit_width, shape)
