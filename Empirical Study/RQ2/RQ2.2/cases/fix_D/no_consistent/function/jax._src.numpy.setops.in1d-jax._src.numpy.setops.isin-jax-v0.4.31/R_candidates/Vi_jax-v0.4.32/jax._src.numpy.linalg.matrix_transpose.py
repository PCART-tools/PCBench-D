def matrix_transpose(x: ArrayLike, /) -> Array:
  """Transpose a matrix or stack of matrices.

  JAX implementation of :func:`numpy.linalg.matrix_transpose`.

  Args:
    x: array of shape ``(..., M, N)``

  Returns:
    array of shape ``(..., N, M)`` containing the matrix transpose of ``x``.

  See also:
    :func:`jax.numpy.transpose`: more general transpose operation.

  Examples:
    Transpose of a single matrix:

    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.linalg.matrix_transpose(x)
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)

    Transpose of a stack of matrices:

    >>> x = jnp.array([[[1, 2],
    ...                 [3, 4]],
    ...                [[5, 6],
    ...                 [7, 8]]])
    >>> jnp.linalg.matrix_transpose(x)
    Array([[[1, 3],
            [2, 4]],
    <BLANKLINE>
           [[5, 7],
            [6, 8]]], dtype=int32)

    For convenience, the same computation can be done via the
    :attr:`~jax.Array.mT` property of JAX array objects:

    >>> x.mT
    Array([[[1, 3],
            [2, 4]],
    <BLANKLINE>
           [[5, 7],
            [6, 8]]], dtype=int32)
  """
  check_arraylike('jnp.linalg.matrix_transpose', x)
  x_arr = jnp.asarray(x)
  ndim = x_arr.ndim
  if ndim < 2:
    raise ValueError(f"matrix_transpose requres at least 2 dimensions; got {ndim=}")
  return jax.lax.transpose(x_arr, (*range(ndim - 2), ndim - 1, ndim - 2))
