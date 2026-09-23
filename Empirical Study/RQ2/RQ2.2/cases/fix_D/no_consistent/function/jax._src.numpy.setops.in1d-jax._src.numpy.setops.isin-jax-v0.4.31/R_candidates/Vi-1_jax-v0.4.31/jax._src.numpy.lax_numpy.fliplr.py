def fliplr(m: ArrayLike) -> Array:
  """Reverse the order of elements of an array along axis 1.

  JAX implementation of :func:`numpy.fliplr`.

  Args:
    m: Array with at least two dimensions.

  Returns:
    An array with the elements in reverse order along axis 1.

  See Also:
    - :func:`jax.numpy.flip`: reverse the order along the given axis
    - :func:`jax.numpy.flipud`: reverse the order along axis 0

  Examples:
    >>> x = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> jnp.fliplr(x)
    Array([[2, 1],
           [4, 3]], dtype=int32)
  """
  util.check_arraylike("fliplr", m)
  return _flip(asarray(m), 1)
