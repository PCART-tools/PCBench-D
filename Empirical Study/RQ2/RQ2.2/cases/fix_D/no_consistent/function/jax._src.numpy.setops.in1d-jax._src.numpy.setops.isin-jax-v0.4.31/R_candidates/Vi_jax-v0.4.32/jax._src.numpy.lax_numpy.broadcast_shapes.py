def broadcast_shapes(*shapes):
  """Broadcast input shapes to a common output shape.

  JAX implementation of :func:`numpy.broadcast_shapes`. JAX uses NumPy-style
  broadcasting rules, which you can read more about at `NumPy broadcasting`_.

  Args:
    shapes: 0 or more shapes specified as sequences of integers

  Returns:
    The broadcasted shape as a tuple of integers.

  See Also:
    - :func:`jax.numpy.broadcast_arrays`: broadcast arrays to a common shape.
    - :func:`jax.numpy.broadcast_to`: broadcast an array to a specified shape.

  Examples:
    Some compatible shapes:

    >>> jnp.broadcast_shapes((1,), (4,))
    (4,)
    >>> jnp.broadcast_shapes((3, 1), (4,))
    (3, 4)
    >>> jnp.broadcast_shapes((3, 1), (1, 4), (5, 1, 1))
    (5, 3, 4)

    Incompatible shapes:

    >>> jnp.broadcast_shapes((3, 1), (4, 1))  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: Incompatible shapes for broadcasting: shapes=[(3, 1), (4, 1)]

  .. _NumPy broadcasting: https://numpy.org/doc/stable/user/basics.broadcasting.html
  """
  if not shapes:
    return ()
  shapes = [(shape,) if np.ndim(shape) == 0 else tuple(shape) for shape in shapes]
  return lax.broadcast_shapes(*shapes)
