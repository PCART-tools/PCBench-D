def multivariate_normal(key: KeyArray,
                        mean: RealArray,
                        cov: RealArray,
                        shape: Optional[Shape] = None,
                        dtype: DTypeLikeFloat = None,
                        method: str = 'cholesky') -> Array:
  r"""Sample multivariate normal random values with given mean and covariance.

  The values are returned according to the probability density function:

  .. math::
     f(x;\mu, \Sigma) = (2\pi)^{-k/2} \det(\Sigma)^{-1}e^{-\frac{1}{2}(x - \mu)^T \Sigma^{-1} (x - \mu)}

  where :math:`k` is the dimension, :math:`\mu` is the mean (given by ``mean``) and
  :math:`\Sigma` is the covariance matrix (given by ``cov``).

  Args:
    key: a PRNG key used as the random key.
    mean: a mean vector of shape ``(..., n)``.
    cov: a positive definite covariance matrix of shape ``(..., n, n)``. The
      batch shape ``...`` must be broadcast-compatible with that of ``mean``.
    shape: optional, a tuple of nonnegative integers specifying the result
      batch shape; that is, the prefix of the result shape excluding the last
      axis. Must be broadcast-compatible with ``mean.shape[:-1]`` and
      ``cov.shape[:-2]``. The default (None) produces a result batch shape by
      broadcasting together the batch shapes of ``mean`` and ``cov``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    method: optional, a method to compute the factor of ``cov``.
      Must be one of 'svd', 'eigh', and 'cholesky'. Default 'cholesky'. For
      singular covariance matrices, use 'svd' or 'eigh'.
  Returns:
    A random array with the specified dtype and shape given by
    ``shape + mean.shape[-1:]`` if ``shape`` is not None, or else
    ``broadcast_shapes(mean.shape[:-1], cov.shape[:-2]) + mean.shape[-1:]``.
  """
  key, _ = _check_prng_key(key)
  mean, cov = promote_dtypes_inexact(mean, cov)
  if method not in {'svd', 'eigh', 'cholesky'}:
    raise ValueError("method must be one of {'svd', 'eigh', 'cholesky'}")
  if dtype is None:
    dtype = mean.dtype
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `multivariate_normal` must be a float "
                     f"dtype, got {dtype}")
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  return _multivariate_normal(key, mean, cov, shape, dtype, method)  # type: ignore
