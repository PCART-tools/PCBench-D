def hsplit(ary: ArrayLike, indices_or_sections: int | Sequence[int] | ArrayLike) -> list[Array]:
  """Split an array into sub-arrays horizontally.

  JAX implementation of :func:`numpy.hsplit`.

  Refer to the documentation of :func:`jax.numpy.split` for details. ``hsplit`` is
  equivalent to ``split`` with ``axis=1``, or ``axis=0`` for one-dimensional arrays.

  Examples:
    1D array:

    >>> x = jnp.array([1, 2, 3, 4, 5, 6])
    >>> x1, x2 = jnp.hsplit(x, 2)
    >>> print(x1, x2)
    [1 2 3] [4 5 6]

    2D array:

    >>> x = jnp.array([[1, 2, 3, 4],
    ...                [5, 6, 7, 8]])
    >>> x1, x2 = jnp.hsplit(x, 2)
    >>> print(x1)
    [[1 2]
     [5 6]]
    >>> print(x2)
    [[3 4]
     [7 8]]

  See also:
    - :func:`jax.numpy.split`: split an array along any axis.
    - :func:`jax.numpy.vsplit`: split vertically, i.e. along axis=0
    - :func:`jax.numpy.dsplit`: split depth-wise, i.e. along axis=2
    - :func:`jax.numpy.array_split`: like ``split``, but allows ``indices_or_sections``
      to be an integer that does not evenly divide the size of the array.
  """
  util.check_arraylike("hsplit", ary)
  a = asarray(ary)
  return _split("hsplit", a, indices_or_sections, axis=0 if a.ndim == 1 else 1)
