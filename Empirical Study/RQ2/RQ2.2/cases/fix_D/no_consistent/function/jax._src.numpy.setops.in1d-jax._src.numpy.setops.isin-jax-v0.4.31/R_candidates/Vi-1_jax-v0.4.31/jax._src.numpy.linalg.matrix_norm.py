def matrix_norm(x: ArrayLike, /, *, keepdims: bool = False, ord: str = 'fro') -> Array:
  """Compute the norm of a matrix or stack of matrices.

  JAX implementation of :func:`numpy.linalg.matrix_norm`

  Args:
    x: array of shape ``(..., M, N)`` for which to take the norm.
    keepdims: if True, keep the reduced dimensions in the output.
    ord: A string or int specifying the type of norm; default is the Frobenius norm.
      See :func:`numpy.linalg.norm` for details on available options.

  Returns:
    array containing the norm of ``x``. Has shape ``x.shape[:-2]`` if ``keepdims`` is
    False, or shape ``(..., 1, 1)`` if ``keepdims`` is True.

  See also:
    - :func:`jax.numpy.linalg.vector_norm`: Norm of a vector or stack of vectors.
    - :func:`jax.numpy.linalg.norm`: More general matrix or vector norm.

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6],
    ...                [7, 8, 9]])
    >>> jnp.linalg.matrix_norm(x)
    Array(16.881943, dtype=float32)
  """
  check_arraylike('jnp.linalg.matrix_norm', x)
  return norm(x, ord=ord, keepdims=keepdims, axis=(-2, -1))
