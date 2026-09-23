def loggamma(key: KeyArray,
             a: RealArray,
             shape: Optional[Sequence[int]] = None,
             dtype: DTypeLikeFloat = dtypes.float_) -> jnp.ndarray:
  """Sample log-gamma random values with given shape and float dtype.

  This function is implemented such that the following will hold for a
  dtype-appropriate tolerance::

    np.testing.assert_allclose(jnp.exp(loggamma(*args)), gamma(*args), rtol=rtol)

  The benefit of log-gamma is that for samples very close to zero (which occur frequently
  when `a << 1`) sampling in log space provides better precision.

  Args:
    key: a PRNG key used as the random key.
    a: a float or array of floats broadcast-compatible with ``shape``
      representing the parameter of the distribution.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``a``. The default (None)
      produces a result shape equal to ``a.shape``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).

  Returns:
    A random array with the specified dtype and with shape given by ``shape`` if
    ``shape`` is not None, or else by ``a.shape``.

  See Also:
    gamma : standard gamma sampler.
  """
  key, _ = _check_prng_key(key)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `gamma` must be a float "
                     f"dtype, got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  return _gamma(key, a, shape=shape, dtype=dtype, log_space=True)
