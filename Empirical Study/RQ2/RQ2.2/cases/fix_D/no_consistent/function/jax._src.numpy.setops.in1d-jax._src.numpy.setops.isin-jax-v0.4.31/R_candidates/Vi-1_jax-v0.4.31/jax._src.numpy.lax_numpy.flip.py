def flip(m: ArrayLike, axis: int | Sequence[int] | None = None) -> Array:
  """Reverse the order of elements of an array along the given axis.

  JAX implementation of :func:`numpy.flip`.

  Args:
    m: Array.
    axis: integer or sequence of integers. Specifies along which axis or axes
      should the array elements be reversed. Default is ``None``, which flips
      along all axes.

  Returns:
    An array with the elements in reverse order along ``axis``.

  See Also:
    - :func:`jax.numpy.fliplr`: reverse the order along axis 1 (left/right)
    - :func:`jax.numpy.flipud`: reverse the order along axis 0 (up/down)

  Examples:
    >>> x1 = jnp.array([[1, 2],
    ...                 [3, 4]])
    >>> jnp.flip(x1)
    Array([[4, 3],
           [2, 1]], dtype=int32)

    If ``axis`` is specified with an integer, then ``jax.numpy.flip`` reverses
    the array along that particular axis only.

    >>> jnp.flip(x1, axis=1)
    Array([[2, 1],
           [4, 3]], dtype=int32)

    >>> x2 = jnp.arange(1, 9).reshape(2, 2, 2)
    >>> x2
    Array([[[1, 2],
            [3, 4]],
    <BLANKLINE>
           [[5, 6],
            [7, 8]]], dtype=int32)
    >>> jnp.flip(x2)
    Array([[[8, 7],
            [6, 5]],
    <BLANKLINE>
           [[4, 3],
            [2, 1]]], dtype=int32)

    When ``axis`` is specified with a sequence of integers, then
    ``jax.numpy.flip`` reverses the array along the specified axes.

    >>> jnp.flip(x2, axis=[1, 2])
    Array([[[4, 3],
            [2, 1]],
    <BLANKLINE>
           [[8, 7],
            [6, 5]]], dtype=int32)
  """
  util.check_arraylike("flip", m)
  return _flip(asarray(m), reductions._ensure_optional_axes(axis))
