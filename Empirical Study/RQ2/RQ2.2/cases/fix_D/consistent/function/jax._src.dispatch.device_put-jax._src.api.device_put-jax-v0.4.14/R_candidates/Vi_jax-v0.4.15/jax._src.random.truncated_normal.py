def truncated_normal(key: KeyArray,
                     lower: RealArray,
                     upper: RealArray,
                     shape: Optional[Union[Shape, NamedShape]] = None,
                     dtype: DTypeLikeFloat = dtypes.float_) -> Array:
  r"""Sample truncated standard normal random values with given shape and dtype.

  The values are returned according to the probability density function:

  .. math::
     f(x) \propto e^{-x^2/2}

  on the domain :math:`\rm{lower} < x < \rm{upper}`.

  Args:
    key: a PRNG key used as the random key.
    lower: a float or array of floats representing the lower bound for
      truncation. Must be broadcast-compatible with ``upper``.
    upper: a float or array of floats representing the  upper bound for
      truncation. Must be broadcast-compatible with ``lower``.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``lower`` and ``upper``. The
      default (None) produces a result shape by broadcasting ``lower`` and
      ``upper``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).

  Returns:
    A random array with the specified dtype and shape given by ``shape`` if
    ``shape`` is not None, or else by broadcasting ``lower`` and ``upper``.
    Returns values in the open interval ``(lower, upper)``.
  """
  key, _ = _check_prng_key(key)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `truncated_normal` must be a float "
                     f"dtype, got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  if shape is not None:
    shape = core.as_named_shape(shape)
  return _truncated_normal(key, lower, upper, shape, dtype)  # type: ignore
