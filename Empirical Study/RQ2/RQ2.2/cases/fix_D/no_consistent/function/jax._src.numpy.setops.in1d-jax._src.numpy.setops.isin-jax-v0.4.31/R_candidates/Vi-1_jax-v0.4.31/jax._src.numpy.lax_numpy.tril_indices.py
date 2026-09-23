def tril_indices(n: int, k: int = 0, m: int | None = None) -> tuple[Array, Array]:
  """Return the indices of lower triangle of an array of size ``(n, m)``.

  JAX implementation of :func:`numpy.tril_indices`.

  Args:
    n: int. Number of rows of the array for which the indices are returned.
    k: optional, int, default=0. Specifies the sub-diagonal on and below which
      the indices of lower triangle are returned. ``k=0`` refers to main diagonal,
      ``k<0`` refers to sub-diagonal below the main diagonal and ``k>0`` refers
      to sub-diagonal above the main diagonal.
    m: optional, int. Number of columns of the array for which the indices are
      returned. If not specified, then ``m = n``.

  Returns:
    A tuple of two arrays containing the indices of the lower triangle, one along
    each axis.

  See also:
    - :func:`jax.numpy.triu_indices`: Returns the indices of upper triangle of an
      array of size ``(n, m)``.
    - :func:`jax.numpy.triu_indices_from`: Returns the indices of upper triangle
      of a given array.
    - :func:`jax.numpy.tril_indices_from`: Returns the indices of lower triangle
      of a given array.

  Examples:
    If only ``n`` is provided in input, the indices of lower triangle of an array
    of size ``(n, n)`` array are returned.

    >>> jnp.tril_indices(3)
    (Array([0, 1, 1, 2, 2, 2], dtype=int32), Array([0, 0, 1, 0, 1, 2], dtype=int32))

    If both ``n`` and ``m`` are provided in input, the indices of lower triangle
    of an ``(n, m)`` array are returned.

    >>> jnp.tril_indices(3, m=2)
    (Array([0, 1, 1, 2, 2], dtype=int32), Array([0, 0, 1, 0, 1], dtype=int32))

    If ``k = 1``, the indices on and below the first sub-diagonal above the main
    diagonal are returned.

    >>> jnp.tril_indices(3, k=1)
    (Array([0, 0, 1, 1, 1, 2, 2, 2], dtype=int32), Array([0, 1, 0, 1, 2, 0, 1, 2], dtype=int32))

    If ``k = -1``, the indices on and below the first sub-diagonal below the main
    diagonal are returned.

    >>> jnp.tril_indices(3, k=-1)
    (Array([1, 2, 2], dtype=int32), Array([0, 0, 1], dtype=int32))
  """
  n = core.concrete_or_error(operator.index, n, "n argument of jnp.triu_indices")
  k = core.concrete_or_error(operator.index, k, "k argument of jnp.triu_indices")
  m = n if m is None else core.concrete_or_error(operator.index, m, "m argument of jnp.triu_indices")
  i, j = nonzero(tril(ones((n, m)), k=k), size=_triu_size(m, n, -k))
  return i, j
