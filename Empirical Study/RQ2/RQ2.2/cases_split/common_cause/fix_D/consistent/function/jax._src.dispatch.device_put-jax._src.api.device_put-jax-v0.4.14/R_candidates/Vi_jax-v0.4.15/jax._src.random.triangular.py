def triangular(key: KeyArray,
               left: RealArray,
               mode: RealArray,
               right: RealArray,
               shape: Optional[Shape] = None,
               dtype: DTypeLikeFloat = dtypes.float_) -> Array:
  r"""Sample Triangular random values with given shape and float dtype.

  The values are returned according to the probability density function:

  .. math::
      f(x; a, b, c) = \frac{2}{c-a} \left\{ \begin{array}{ll} \frac{x-a}{b-a} & a \leq x \leq b \\ \frac{c-x}{c-b} & b \leq x \leq c \end{array} \right.

  on the domain :math:`a \leq x \leq c`.

  Args:
    key: a PRNG key used as the random key.
    left: a float or array of floats broadcast-compatible with ``shape``
      representing the lower limit parameter of the distribution.
    mode: a float or array of floats broadcast-compatible with ``shape``
      representing the peak value parameter of the distribution, value must
      fulfill the condition ``left <= mode <= right``.
    right: a float or array of floats broadcast-compatible with ``shape``
      representing the upper limit parameter of the distribution, must be
      larger than ``left``.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``left``,``mode`` and ``right``.
      The default (None) produces a result shape equal to ``left.shape``, ``mode.shape``
      and ``right.shape``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).

  Returns:
    A random array with the specified dtype and with shape given by ``shape`` if
    ``shape`` is not None, or else by ``left.shape``, ``mode.shape`` and ``right.shape``.
  """
  key, _ = _check_prng_key(key)
  dtypes.check_user_dtype_supported(dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError("dtype argument to `triangular` must be a float "
                     f"dtype, got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  return _triangular(key, left, mode, right, shape, dtype)
