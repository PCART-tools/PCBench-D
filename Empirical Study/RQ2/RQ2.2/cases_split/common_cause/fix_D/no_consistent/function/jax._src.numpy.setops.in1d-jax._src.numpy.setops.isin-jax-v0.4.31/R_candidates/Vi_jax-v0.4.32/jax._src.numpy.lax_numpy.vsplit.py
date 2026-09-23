def vsplit(ary: ArrayLike, indices_or_sections: int | Sequence[int] | ArrayLike) -> list[Array]:
  """Split an array into sub-arrays vertically.

  JAX implementation of :func:`numpy.vsplit`.

  Refer to the documentation of :func:`jax.numpy.split` for details; ``vsplit`` is
  equivalent to ``split`` with ``axis=0``.

  Examples:
    1D array:

    >>> x = jnp.array([1, 2, 3, 4, 5, 6])
    >>> x1, x2 = jnp.vsplit(x, 2)
    >>> print(x1, x2)
    [1 2 3] [4 5 6]

    2D array:

    >>> x = jnp.array([[1, 2, 3, 4],
    ...                [5, 6, 7, 8]])
    >>> x1, x2 = jnp.vsplit(x, 2)
    >>> print(x1, x2)
    [[1 2 3 4]] [[5 6 7 8]]

  See also:
    - :func:`jax.numpy.split`: split an array along any axis.
    - :func:`jax.numpy.hsplit`: split horizontally, i.e. along axis=1
    - :func:`jax.numpy.dsplit`: split depth-wise, i.e. along axis=2
    - :func:`jax.numpy.array_split`: like ``split``, but allows ``indices_or_sections``
      to be an integer that does not evenly divide the size of the array.
  """
  return _split("vsplit", ary, indices_or_sections, axis=0)
