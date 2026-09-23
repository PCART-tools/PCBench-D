def split(ary: ArrayLike, indices_or_sections: int | Sequence[int] | ArrayLike,
          axis: int = 0) -> list[Array]:
  """Split an array into sub-arrays.

  JAX implementation of :func:`numpy.split`.

  Args:
    ary: N-dimensional array-like object to split
    indices_or_sections: either a single integer or a sequence of indices.

      - if ``indices_or_sections`` is an integer *N*, then *N* must evenly divide
        ``ary.shape[axis]`` and ``ary`` will be divided into *N* equally-sized
        chunks along ``axis``.
      - if ``indices_or_sections`` is a sequence of integers, then these integers
        specify the boundary between unevenly-sized chunks along ``axis``; see
        examples below.

    axis: the axis along which to split; defaults to 0.

  Returns:
    A list of arrays. If ``indices_or_sections`` is an integer *N*, then the list is
    of length *N*. If ``indices_or_sections`` is a sequence *seq*, then the list is
    is of length *len(seq) + 1*.

  Examples:
    Splitting a 1-dimensional array:

    >>> x = jnp.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

    Split into three equal sections:

    >>> chunks = jnp.split(x, 3)
    >>> print(*chunks)
    [1 2 3] [4 5 6] [7 8 9]

    Split into sections by index:

    >>> chunks = jnp.split(x, [2, 7])  # [x[0:2], x[2:7], x[7:]]
    >>> print(*chunks)
    [1 2] [3 4 5 6 7] [8 9]

    Splitting a two-dimensional array along axis 1:

    >>> x = jnp.array([[1, 2, 3, 4],
    ...                [5, 6, 7, 8]])
    >>> x1, x2 = jnp.split(x, 2, axis=1)
    >>> print(x1)
    [[1 2]
     [5 6]]
    >>> print(x2)
    [[3 4]
     [7 8]]

  See also:
    - :func:`jax.numpy.array_split`: like ``split``, but allows ``indices_or_sections``
      to be an integer that does not evenly divide the size of the array.
    - :func:`jax.numpy.vsplit`: split vertically, i.e. along axis=0
    - :func:`jax.numpy.hsplit`: split horizontally, i.e. along axis=1
    - :func:`jax.numpy.dsplit`: split depth-wise, i.e. along axis=2
  """
  return _split("split", ary, indices_or_sections, axis=axis)
