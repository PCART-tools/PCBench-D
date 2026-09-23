def tril_indices_from(arr: ArrayLike, k: int = 0) -> tuple[Array, Array]:
  """Return the indices of lower triangle of a given array.

  JAX implementation of :func:`numpy.tril_indices_from`.

  Args:
    arr: input array. Must have ``arr.ndim == 2``.
    k: optional, int, default=0. Specifies the sub-diagonal on and below which
      the indices of upper triangle are returned. ``k=0`` refers to main diagonal,
      ``k<0`` refers to sub-diagonal below the main diagonal and ``k>0`` refers
      to sub-diagonal above the main diagonal.

  Returns:
    A tuple of two arrays containing the indices of the lower triangle, one along
    each axis.

  See also:
    - :func:`jax.numpy.triu_indices_from`: Returns the indices of upper triangle
      of a given array.
    - :func:`jax.numpy.tril_indices`: Returns the indices of lower triangle of an
      array of size ``(n, m)``.
    - :func:`jax.numpy.tril`: Returns a lower triangle of an array

  Examples:
    >>> arr = jnp.array([[1, 2, 3],
    ...                  [4, 5, 6],
    ...                  [7, 8, 9]])
    >>> jnp.tril_indices_from(arr)
    (Array([0, 1, 1, 2, 2, 2], dtype=int32), Array([0, 0, 1, 0, 1, 2], dtype=int32))

    Elements indexed by ``jnp.tril_indices_from`` correspond to those in the
    output of ``jnp.tril``.

    >>> ind = jnp.tril_indices_from(arr)
    >>> arr[ind]
    Array([1, 4, 5, 7, 8, 9], dtype=int32)
    >>> jnp.tril(arr)
    Array([[1, 0, 0],
           [4, 5, 0],
           [7, 8, 9]], dtype=int32)

    When ``k > 0``:

    >>> jnp.tril_indices_from(arr, k=1)
    (Array([0, 0, 1, 1, 1, 2, 2, 2], dtype=int32), Array([0, 1, 0, 1, 2, 0, 1, 2], dtype=int32))

    When ``k < 0``:

    >>> jnp.tril_indices_from(arr, k=-1)
    (Array([1, 2, 2], dtype=int32), Array([0, 0, 1], dtype=int32))
  """
  arr_shape = shape(arr)
  if len(arr_shape) != 2:
    raise ValueError("Only 2-D inputs are accepted")
  return tril_indices(arr_shape[0], k=k, m=arr_shape[1])
