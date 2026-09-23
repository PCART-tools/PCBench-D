def broadcast_arrays(*args: ArrayLike) -> list[Array]:
  """Broadcast arrays to a common shape.

  JAX implementation of :func:`numpy.broadcast_arrays`. JAX uses NumPy-style
  broadcasting rules, which you can read more about at `NumPy broadcasting`_.

  Args:
    args: zero or more array-like objects to be broadcasted.

  Returns:
    a list of arrays containing broadcasted copies of the inputs.

  See also:
    - :func:`jax.numpy.broadcast_shapes`: broadcast input shapes to a common shape.
    - :func:`jax.numpy.broadcast_to`: broadcast an array to a specified shape.

  Examples:

    >>> x = jnp.arange(3)
    >>> y = jnp.int32(1)
    >>> jnp.broadcast_arrays(x, y)
    [Array([0, 1, 2], dtype=int32), Array([1, 1, 1], dtype=int32)]

    >>> x = jnp.array([[1, 2, 3]])
    >>> y = jnp.array([[10],
    ...                [20]])
    >>> x2, y2 = jnp.broadcast_arrays(x, y)
    >>> x2
    Array([[1, 2, 3],
           [1, 2, 3]], dtype=int32)
    >>> y2
    Array([[10, 10, 10],
           [20, 20, 20]], dtype=int32)

  .. _NumPy broadcasting: https://numpy.org/doc/stable/user/basics.broadcasting.html
  """
  return util._broadcast_arrays(*args)
