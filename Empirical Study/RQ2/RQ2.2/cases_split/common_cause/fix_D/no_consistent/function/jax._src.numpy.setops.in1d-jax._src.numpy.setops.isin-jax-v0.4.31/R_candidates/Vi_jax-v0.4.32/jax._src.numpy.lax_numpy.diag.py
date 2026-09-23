def diag(v: ArrayLike, k: int = 0) -> Array:
  """Returns the specified diagonal or constructs a diagonal array.

  JAX implementation of :func:`numpy.diag`.

  The JAX version always returns a copy of the input, although if this is used
  within a JIT compilation, the compiler may avoid the copy.

  Args:
    v: Input array. Can be a 1-D array to create a diagonal matrix or a
      2-D array to extract a diagonal.
    k: optional, default=0. Diagonal offset. Positive values place the diagonal
      above the main diagonal, negative values place it below the main diagonal.

  Returns:
    If `v` is a 2-D array, a 1-D array containing the diagonal elements.
    If `v` is a 1-D array, a 2-D array with the input elements placed along the
    specified diagonal.

  See also:
    - :func:`jax.numpy.diagflat`
    - :func:`jax.numpy.diagonal`

  Examples:
    Creating a diagonal matrix from a 1-D array:

    >>> jnp.diag(jnp.array([1, 2, 3]))
    Array([[1, 0, 0],
           [0, 2, 0],
           [0, 0, 3]], dtype=int32)

    Specifying a diagonal offset:

    >>> jnp.diag(jnp.array([1, 2, 3]), k=1)
    Array([[0, 1, 0, 0],
           [0, 0, 2, 0],
           [0, 0, 0, 3],
           [0, 0, 0, 0]], dtype=int32)

    Extracting a diagonal from a 2-D array:

    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6],
    ...                [7, 8, 9]])
    >>> jnp.diag(x)
    Array([1, 5, 9], dtype=int32)
  """
  return _diag(v, operator.index(k))
