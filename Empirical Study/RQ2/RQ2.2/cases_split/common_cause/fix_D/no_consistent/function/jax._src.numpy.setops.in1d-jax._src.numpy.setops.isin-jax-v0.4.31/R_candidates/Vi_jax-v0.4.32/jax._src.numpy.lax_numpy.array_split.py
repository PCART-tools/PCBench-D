def array_split(ary: ArrayLike, indices_or_sections: int | Sequence[int] | ArrayLike,
                axis: int = 0) -> list[Array]:
  """Split an array into sub-arrays.

  JAX implementation of :func:`numpy.array_split`.

  Refer to the documentation of :func:`jax.numpy.split` for details; ``array_split``
  is equivalent to ``split``, but allows integer ``indices_or_sections`` which does
  not evenly divide the split axis.

  Examples:
    >>> x = jnp.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> chunks = jnp.array_split(x, 4)
    >>> print(*chunks)
    [1 2 3] [4 5] [6 7] [8 9]

  See also:
    - :func:`jax.numpy.split`: split an array along any axis.
    - :func:`jax.numpy.vsplit`: split vertically, i.e. along axis=0
    - :func:`jax.numpy.hsplit`: split horizontally, i.e. along axis=1
    - :func:`jax.numpy.dsplit`: split depth-wise, i.e. along axis=2
  """
  return _split("array_split", ary, indices_or_sections, axis=axis)
