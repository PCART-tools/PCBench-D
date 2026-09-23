def dsplit(ary: ArrayLike, indices_or_sections: int | Sequence[int] | ArrayLike) -> list[Array]:
  """Split an array into sub-arrays depth-wise.

  JAX implementation of :func:`numpy.dsplit`.

  Refer to the documentation of :func:`jax.numpy.split` for details. ``dsplit`` is
  equivalent to ``split`` with ``axis=2``.

  Examples:

    >>> x = jnp.arange(12).reshape(3, 1, 4)
    >>> print(x)
    [[[ 0  1  2  3]]
    <BLANKLINE>
     [[ 4  5  6  7]]
    <BLANKLINE>
     [[ 8  9 10 11]]]
    >>> x1, x2 = jnp.dsplit(x, 2)
    >>> print(x1)
    [[[0 1]]
    <BLANKLINE>
     [[4 5]]
    <BLANKLINE>
     [[8 9]]]
    >>> print(x2)
    [[[ 2  3]]
    <BLANKLINE>
     [[ 6  7]]
    <BLANKLINE>
     [[10 11]]]

  See also:
    - :func:`jax.numpy.split`: split an array along any axis.
    - :func:`jax.numpy.vsplit`: split vertically, i.e. along axis=0
    - :func:`jax.numpy.hsplit`: split horizontally, i.e. along axis=1
    - :func:`jax.numpy.array_split`: like ``split``, but allows ``indices_or_sections``
      to be an integer that does not evenly divide the size of the array.
  """
  return _split("dsplit", ary, indices_or_sections, axis=2)
