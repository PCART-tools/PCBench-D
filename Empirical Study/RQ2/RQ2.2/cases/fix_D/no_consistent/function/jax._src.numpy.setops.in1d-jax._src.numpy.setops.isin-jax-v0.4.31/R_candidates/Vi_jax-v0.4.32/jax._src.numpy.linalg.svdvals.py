def svdvals(x: ArrayLike, /) -> Array:
  """Compute the singular values of a matrix.

  JAX implementation of :func:`numpy.linalg.svdvals`.

  Args:
    x: array of shape ``(..., M, N)`` for which singular values will be computed.

  Returns:
    array of singular values of shape ``(..., K)`` with ``K = min(M, N)``.

  See also:
    :func:`jax.numpy.linalg.svd`: compute singular values and singular vectors

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.linalg.svdvals(x)
    Array([9.508031 , 0.7728694], dtype=float32)
  """
  check_arraylike('jnp.linalg.svdvals', x)
  return svd(x, compute_uv=False, hermitian=False)
