def flipud(m: ArrayLike) -> Array:
  """Reverse the order of elements of an array along axis 0.

  JAX implementation of :func:`numpy.flipud`.

  Args:
    m: Array with at least one dimension.

  Returns:
    An array with the elements in reverse order along axis 0.

  See Also:
    - :func:`jax.numpy.flip`: reverse the order along the given axis
    - :func:`jax.numpy.fliplr`: reverse the order along axis 1

  Examples:
    >>> x = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> jnp.flipud(x)
    Array([[3, 4],
           [1, 2]], dtype=int32)
  """
  util.check_arraylike("flipud", m)
  return _flip(asarray(m), 0)
