def maxwell(key: KeyArray,
            shape: Shape = (),
            dtype: DTypeLikeFloat = dtypes.float_) -> Array:
  """Sample from a one sided Maxwell distribution.

  The scipy counterpart is `scipy.stats.maxwell`.

  Args:
    key: a PRNG key.
    shape: The shape of the returned samples.
    dtype: The type used for samples.

  Returns:
    A jnp.array of samples, of shape `shape`.

  """
  # Generate samples using:
  # sqrt(X^2 + Y^2 + Z^2), X,Y,Z ~N(0,1)
  key, _ = _check_prng_key(key)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `maxwell` must be a float "
                     f"dtype, got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  shape = core.canonicalize_shape(shape)
  return _maxwell(key, shape, dtype)
