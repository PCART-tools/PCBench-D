def uniform(key: KeyArray,
            shape: Union[Sequence[int], NamedShape] = (),
            dtype: DTypeLikeFloat = dtypes.float_,
            minval: RealArray = 0.,
            maxval: RealArray = 1.) -> jnp.ndarray:
  """Sample uniform random values in [minval, maxval) with given shape/dtype.

  Args:
    key: a PRNG key used as the random key.
    shape: optional, a tuple of nonnegative integers representing the result
      shape. Default ().
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    minval: optional, a minimum (inclusive) value broadcast-compatible with shape for the range (default 0).
    maxval: optional, a maximum (exclusive) value broadcast-compatible with shape for the range (default 1).

  Returns:
    A random array with the specified shape and dtype.
  """
  key, _ = _check_prng_key(key)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `uniform` must be a float dtype, "
                     f"got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  shape = core.as_named_shape(shape)
  return _uniform(key, shape, dtype, minval, maxval)  # type: ignore
