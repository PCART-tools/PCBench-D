@jit
def fmin(x1: ArrayLike, x2: ArrayLike) -> Array:
  """Return element-wise minimum of the input arrays.

  JAX implemtentation of :func:`numpy.fmin`.

  Args:
    x1: input array or scalar.
    x2: input array or scalar. x1 and x2 must either have same shape or be
      broadcast compatible.

  Returns:
    An array containing the element-wise minimum of x1 and x2.

  Note:
    For each pair of elements, ``jnp.fmin`` returns:
      - the smaller of the two if both elements are finite numbers.
      - finite number if one element is ``nan``.
      - ``-inf`` if one element is ``-inf`` and the other is finite or ``nan``.
      - ``inf`` if one element is ``inf`` and the other is ``nan``.
      - ``nan`` if both elements are ``nan``.

  Examples:
    >>> jnp.fmin(2, 3)
    Array(2, dtype=int32, weak_type=True)
    >>> jnp.fmin(2, jnp.array([1, 4, 2, -1]))
    Array([ 1,  2,  2, -1], dtype=int32)

    >>> x1 = jnp.array([1, 3, 2])
    >>> x2 = jnp.array([2, 1, 4])
    >>> jnp.fmin(x1, x2)
    Array([1, 1, 2], dtype=int32)

    >>> x3 = jnp.array([1, 5, 3])
    >>> x4 = jnp.array([[2, 3, 1],
    ...                 [5, 6, 7]])
    >>> jnp.fmin(x3, x4)
    Array([[1, 3, 1],
           [1, 5, 3]], dtype=int32)

    >>> nan = jnp.nan
    >>> x5 = jnp.array([jnp.inf, 5, nan])
    >>> x6 = jnp.array([[2, 3, nan],
    ...                 [nan, 6, 7]])
    >>> jnp.fmin(x5, x6)
    Array([[ 2.,  3., nan],
           [inf,  5.,  7.]], dtype=float32)
  """
  return where(ufuncs.less(x1, x2) | ufuncs.isnan(x2), x1, x2)
