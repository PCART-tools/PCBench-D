def weibull_min(key: KeyArray,
                scale: RealArray,
                concentration: RealArray,
                shape: Sequence[int] = (),
                dtype: DTypeLikeFloat = dtypes.float_) -> jnp.ndarray:
  """Sample from a Weibull distribution.

  The scipy counterpart is `scipy.stats.weibull_min`.

  Args:
    key: a PRNG key.
    scale: The scale parameter of the distribution.
    concentration: The concentration parameter of the distribution.
    shape: The shape added to the parameters loc and scale broadcastable shape.
    dtype: The type used for samples.

  Returns:
    A jnp.array of samples.

  """
  key, _ = _check_prng_key(key)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `weibull_min` must be a float "
                     f"dtype, got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  shape = core.canonicalize_shape(shape)
  return _weibull_min(key, scale, concentration, shape, dtype)
