def dirichlet(key: KeyArray,
              alpha: RealArray,
              shape: Optional[Shape] = None,
              dtype: DTypeLikeFloat = dtypes.float_) -> Array:
  r"""Sample Dirichlet random values with given shape and float dtype.

  The values are distributed according the the probability density function:

  .. math::
     f(\{x_i\}; \{\alpha_i\}) = \propto \prod_{i=1}^k x_i^{\alpha_i}

  Where :math:`k` is the dimension, and :math:`\{x_i\}` satisfies

  .. math::
     \sum_{i=1}^k x_i = 1

  and :math:`0 \le x_i \le 1` for all :math:`x_i`.

  Args:
    key: a PRNG key used as the random key.
    alpha: an array of shape ``(..., n)`` used as the concentration
      parameter of the random variables.
    shape: optional, a tuple of nonnegative integers specifying the result
      batch shape; that is, the prefix of the result shape excluding the last
      element of value ``n``. Must be broadcast-compatible with
      ``alpha.shape[:-1]``. The default (None) produces a result shape equal to
      ``alpha.shape``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).

  Returns:
    A random array with the specified dtype and shape given by
    ``shape + (alpha.shape[-1],)`` if ``shape`` is not None, or else
    ``alpha.shape``.
  """
  key, _ = _check_prng_key(key)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `dirichlet` must be a float "
                     f"dtype, got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  return _dirichlet(key, alpha, shape, dtype)
