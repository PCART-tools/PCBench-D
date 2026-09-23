@jit
def matrix_rank(
  M: ArrayLike, rtol: ArrayLike | None = None, *,
  tol: ArrayLike | DeprecatedArg | None = DeprecatedArg()) -> Array:
  """Compute the rank of a matrix.

  JAX implementation of :func:`numpy.linalg.matrix_rank`.

  The rank is calculated via the Singular Value Decomposition (SVD), and determined
  by the number of singular values greater than the specified tolerance.

  Args:
    M: array of shape ``(..., N, K)`` whose rank is to be computed.
    rtol: optional array of shape ``(...)`` specifying the tolerance. Singular values
      smaller than `rtol * largest_singular_value` are considered to be zero. If
      ``rtol`` is None (the default), a reasonable default is chosen based the
      floating point precision of the input.

  Returns:
    array of shape ``a.shape[-2]`` giving the matrix rank.

  Notes:
    The rank calculation may be inaccurate for matrices with very small singular
    values or those that are numerically ill-conditioned. Consider adjusting the
    ``rtol`` parameter or using a more specialized rank computation method in such cases.

  Examples:
    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> jnp.linalg.matrix_rank(a)
    Array(2, dtype=int32)

    >>> b = jnp.array([[1, 0],  # Rank-deficient matrix
    ...                [0, 0]])
    >>> jnp.linalg.matrix_rank(b)
    Array(1, dtype=int32)
  """
  check_arraylike("jnp.linalg.matrix_rank", M)
  # TODO(micky774): deprecated 2024-5-14, remove after deprecation expires.
  if not isinstance(tol, DeprecatedArg):
    rtol = tol
    del tol
    warnings.warn(
      "The tol argument for linalg.matrix_rank is deprecated using it will soon raise "
      "an error. To prepare for future releases, and suppress this warning, "
      "please use rtol instead.",
      DeprecationWarning, stacklevel=2
    )
  M, = promote_dtypes_inexact(jnp.asarray(M))
  if M.ndim < 2:
    return (M != 0).any().astype(jnp.int32)
  S = svd(M, full_matrices=False, compute_uv=False)
  if rtol is None:
    rtol = S.max(-1) * np.max(M.shape[-2:]).astype(S.dtype) * jnp.finfo(S.dtype).eps
  rtol = jnp.expand_dims(rtol, np.ndim(rtol))
  return reductions.sum(S > rtol, axis=-1)
