def broadcast_to(array: ArrayLike, shape: DimSize | Shape) -> Array:
  """Broadcast an array to a specified shape.

  JAX implementation of :func:`numpy.broadcast_to`. JAX uses NumPy-style
  broadcasting rules, which you can read more about at `NumPy broadcasting`_.

  Args:
    array: array to be broadcast.
    shape: shape to which the array will be broadcast.

  Returns:
    a copy of array broadcast to the specified shape.

  See also:
    - :func:`jax.numpy.broadcast_arrays`: broadcast arrays to a common shape.
    - :func:`jax.numpy.broadcast_shapes`: broadcast input shapes to a common shape.

  Examples:
    >>> x = jnp.int32(1)
    >>> jnp.broadcast_to(x, (1, 4))
    Array([[1, 1, 1, 1]], dtype=int32)

    >>> x = jnp.array([1, 2, 3])
    >>> jnp.broadcast_to(x, (2, 3))
    Array([[1, 2, 3],
           [1, 2, 3]], dtype=int32)

    >>> x = jnp.array([[2], [4]])
    >>> jnp.broadcast_to(x, (2, 4))
    Array([[2, 2, 2, 2],
           [4, 4, 4, 4]], dtype=int32)

  .. _NumPy broadcasting: https://numpy.org/doc/stable/user/basics.broadcasting.html
  """
  return util._broadcast_to(array, shape)
