def diag_indices_from(arr: ArrayLike) -> tuple[Array, ...]:
  """Return indices for accessing the main diagonal of a given array.

  JAX implementation of :func:`numpy.diag_indices_from`.

  Args:
    arr: Input array. Must be at least 2-dimensional and have equal length along
      all dimensions.

  Returns:
    A tuple of arrays containing the indices to access the main diagonal of
    the input array.

  See also:
    - :func:`jax.numpy.diag_indices`
    - :func:`jax.numpy.diagonal`

  Examples:
    >>> arr = jnp.array([[1, 2, 3],
    ...                  [4, 5, 6],
    ...                  [7, 8, 9]])
    >>> jnp.diag_indices_from(arr)
    (Array([0, 1, 2], dtype=int32), Array([0, 1, 2], dtype=int32))
    >>> arr = jnp.array([[[1, 2], [3, 4]],
    ...                  [[5, 6], [7, 8]]])
    >>> jnp.diag_indices_from(arr)
    (Array([0, 1], dtype=int32),
    Array([0, 1], dtype=int32),
    Array([0, 1], dtype=int32))
  """
  util.check_arraylike("diag_indices_from", arr)
  nd = ndim(arr)
  if not ndim(arr) >= 2:
    raise ValueError("input array must be at least 2-d")

  s = shape(arr)
  if len(set(shape(arr))) != 1:
    raise ValueError("All dimensions of input must be of equal length")

  return diag_indices(s[0], ndim=nd)
