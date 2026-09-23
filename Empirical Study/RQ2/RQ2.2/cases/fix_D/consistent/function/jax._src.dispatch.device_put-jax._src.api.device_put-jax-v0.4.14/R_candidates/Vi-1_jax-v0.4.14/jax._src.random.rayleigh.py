def rayleigh(key: KeyArray,
             scale: RealArray,
             shape: Optional[Shape] = None,
             dtype: DTypeLikeFloat = dtypes.float_) -> Array:
  r"""Sample Rayleigh random values with given shape and float dtype.

  The values are returned according to the probability density function:

  .. math::
     f(x;\sigma) \propto xe^{-x^2/(2\sigma^2)}

  on the domain :math:`-\infty < x < \infty`, and where `\sigma > 0` is the scale
  parameter of the distribution.

  Args:
    key: a PRNG key used as the random key.
    scale: a float or array of floats broadcast-compatible with ``shape``
      representing the parameter of the distribution.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``scale``. The default (None)
      produces a result shape equal to ``scale.shape``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).

  Returns:
    A random array with the specified dtype and with shape given by ``shape`` if
    ``shape`` is not None, or else by ``scale.shape``.
  """
  key, _ = _check_prng_key(key)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError("dtype argument to `rayleigh` must be a float "
                     f"dtype, got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  return _rayleigh(key, scale, shape, dtype)
