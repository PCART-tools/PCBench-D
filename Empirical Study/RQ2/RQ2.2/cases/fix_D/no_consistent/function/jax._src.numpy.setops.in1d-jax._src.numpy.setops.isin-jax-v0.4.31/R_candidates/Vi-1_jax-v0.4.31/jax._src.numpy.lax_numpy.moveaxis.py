def moveaxis(a: ArrayLike, source: int | Sequence[int],
             destination: int | Sequence[int]) -> Array:
  """Move an array axis to a new position

  JAX implementation of :func:`numpy.moveaxis`, implemented in terms of
  :func:`jax.lax.transpose`.

  Args:
    a: input array
    source: index or indices of the axes to move.
    destination: index or indices of the axes destinations

  Returns:
    Copy of ``a`` with axes moved from ``source`` to ``destination``.

  Notes:
    Unlike :func:`numpy.moveaxis`, :func:`jax.numpy.moveaxis` will return a copy rather
    than a view of the input array. However, under JIT, the compiler will optimize away
    such copies when possible, so this doesn't have performance impacts in practice.

  See also:
    - :func:`jax.numpy.swapaxes`: swap two axes.
    - :func:`jax.numpy.rollaxis`: older API for moving an axis.
    - :func:`jax.numpy.transpose`: general axes permutation.

  Examples:
    >>> a = jnp.ones((2, 3, 4, 5))

    Move axis ``1`` to the end of the array:

    >>> jnp.moveaxis(a, 1, -1).shape
    (2, 4, 5, 3)

    Move the last axis to position 1:

    >>> jnp.moveaxis(a, -1, 1).shape
    (2, 5, 3, 4)

    Move multiple axes:

    >>> jnp.moveaxis(a, (0, 1), (-1, -2)).shape
    (4, 5, 3, 2)

    This can also be accomplished via :func:`~jax.numpy.transpose`:

    >>> a.transpose(2, 3, 1, 0).shape
    (4, 5, 3, 2)
  """
  util.check_arraylike("moveaxis", a)
  return _moveaxis(asarray(a), _ensure_index_tuple(source),
                   _ensure_index_tuple(destination))
