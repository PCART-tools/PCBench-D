def matrix_transpose(x: ArrayLike, /) -> Array:
  """Transpose the last two dimensions of an array.

  JAX implementation of :func:`numpy.matrix_transpose`, implemented in terms of
  :func:`jax.lax.transpose`.

  Args:
    x: input array, Must have ``x.ndim >= 2``

  Returns:
    matrix-transposed copy of the array.

  See Also:
    - :attr:`jax.Array.mT`: same operation accessed via an :func:`~jax.Array` property.
    - :func:`jax.numpy.transpose`: general multi-axis transpose

  Note:
    Unlike :func:`numpy.matrix_transpose`, :func:`jax.numpy.matrix_transpose` will return a
    copy rather than a view of the input array. However, under JIT, the compiler will
    optimize-away such copies when possible, so this doesn't have performance impacts in practice.

  Examples:
    Here is a 2x2x2 matrix representing a batched 2x2 matrix:

    >>> x = jnp.array([[[1, 2],
    ...                 [3, 4]],
    ...                [[5, 6],
    ...                 [7, 8]]])
    >>> jnp.matrix_transpose(x)
    Array([[[1, 3],
            [2, 4]],
    <BLANKLINE>
           [[5, 7],
            [6, 8]]], dtype=int32)

    For convenience, you can perform the same transpose via the :attr:`~jax.Array.mT`
    property of :class:`jax.Array`:

    >>> x.mT
    Array([[[1, 3],
            [2, 4]],
    <BLANKLINE>
           [[5, 7],
            [6, 8]]], dtype=int32)
  """
  util.check_arraylike("matrix_transpose", x)
  ndim = np.ndim(x)
  if ndim < 2:
    raise ValueError(f"x must be at least two-dimensional for matrix_transpose; got {ndim=}")
  axes = (*range(ndim - 2), ndim - 1, ndim - 2)
  return lax.transpose(x, axes)
