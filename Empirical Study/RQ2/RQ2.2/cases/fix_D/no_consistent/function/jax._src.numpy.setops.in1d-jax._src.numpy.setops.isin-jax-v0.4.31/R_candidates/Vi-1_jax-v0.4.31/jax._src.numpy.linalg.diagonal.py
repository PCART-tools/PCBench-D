def diagonal(x: ArrayLike, /, *, offset: int = 0) -> Array:
  """Extract the diagonal of an matrix or stack of matrices.

  JAX implementation of :func:`numpy.linalg.diagonal`.

  Args:
    x: array of shape ``(..., M, N)`` from which the diagonal will be extracted.
    offset: positive or negative offset from the main diagonal.

  Returns:
    Array of shape ``(..., K)`` where ``K`` is the length of the specified diagonal.

  See Also:
    - :func:`jax.numpy.diagonal`: more general functionality for extracting diagonals.
    - :func:`jax.numpy.diag`: create a diagonal matrix from values.

  Examples:
    Diagonals of a single matrix:

    >>> x = jnp.array([[1,  2,  3,  4],
    ...                [5,  6,  7,  8],
    ...                [9, 10, 11, 12]])
    >>> jnp.linalg.diagonal(x)
    Array([ 1,  6, 11], dtype=int32)
    >>> jnp.linalg.diagonal(x, offset=1)
    Array([ 2,  7, 12], dtype=int32)
    >>> jnp.linalg.diagonal(x, offset=-1)
    Array([ 5, 10], dtype=int32)

    Batched diagonals:

    >>> x = jnp.arange(24).reshape(2, 3, 4)
    >>> jnp.linalg.diagonal(x)
    Array([[ 0,  5, 10],
           [12, 17, 22]], dtype=int32)
  """
  check_arraylike('jnp.linalg.diagonal', x)
  return jnp.diagonal(x, offset=offset, axis1=-2, axis2=-1)
