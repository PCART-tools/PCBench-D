def permute_dims(a: ArrayLike, /, axes: tuple[int, ...]) -> Array:
  """Permute the axes/dimensions of an array.

  JAX implementation of :func:`array_api.permute_dims`.

  Args:
    a: input array
    axes: tuple of integers in range ``[0, a.ndim)`` specifying the
      axes permutation.

  Returns:
    a copy of ``a`` with axes permuted.

  See also:
    - :func:`jax.numpy.transpose`
    - :func:`jax.numpy.matrix_transpose`

  Examples:
    >>> a = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.permute_dims(a, (1, 0))
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)
  """
  util.check_arraylike("permute_dims", a)
  return lax.transpose(a, axes)
