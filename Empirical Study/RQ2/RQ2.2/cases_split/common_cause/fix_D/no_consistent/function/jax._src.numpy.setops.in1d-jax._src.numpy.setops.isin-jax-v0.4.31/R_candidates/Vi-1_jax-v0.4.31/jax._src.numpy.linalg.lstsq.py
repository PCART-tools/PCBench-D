def lstsq(a: ArrayLike, b: ArrayLike, rcond: float | None = None, *,
          numpy_resid: bool = False) -> tuple[Array, Array, Array, Array]:
  """
  Return the least-squares solution to a linear equation.

  JAX implementation of :func:`numpy.linalg.lstsq`.

  Args:
    a: array of shape ``(M, N)`` representing the coefficient matrix.
    b: array of shape ``(M,)`` or ``(M, K)`` representing the right-hand side.
    rcond: Cut-off ratio for small singular values. Singular values smaller than
      ``rcond * largest_singular_value`` are treated as zero. If None (default),
      the optimal value will be used to reduce floating point errors.
    numpy_resid: If True, compute and return residuals in the same way as NumPy's
      `linalg.lstsq`. This is necessary if you want to precisely replicate NumPy's
      behavior. If False (default), a more efficient method is used to compute residuals.

  Returns:
    Tuple of arrays ``(x, resid, rank, s)`` where

    - ``x`` is a shape ``(N,)`` or ``(N, K)`` array containing the least-squares solution.
    - ``resid`` is the sum of squared residual of shape ``()`` or ``(K,)``.
    - ``rank`` is the rank of the matrix ``a``.
    - ``s`` is the singular values of the matrix ``a``.

  Examples:
    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> b = jnp.array([5, 6])
    >>> x, _, _, _ = jnp.linalg.lstsq(a, b)
    >>> with jnp.printoptions(precision=3):
    ...   print(x)
    [-4.   4.5]
  """
  check_arraylike("jnp.linalg.lstsq", a, b)
  if numpy_resid:
    return _lstsq(a, b, rcond, numpy_resid=True)
  return _jit_lstsq(a, b, rcond)
