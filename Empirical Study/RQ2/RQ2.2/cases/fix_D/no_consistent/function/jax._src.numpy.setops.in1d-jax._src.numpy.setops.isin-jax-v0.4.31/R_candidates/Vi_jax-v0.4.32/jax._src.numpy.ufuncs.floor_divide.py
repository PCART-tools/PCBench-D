@jit
def floor_divide(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Calculates the floor division of x1 by x2 element-wise

  JAX implementation of :obj:`numpy.floor_divide`.

  Args:
    x1: Input array, the dividend
    x2: Input array, the divisor

  Returns:
    An array-like object containing each of the quotients rounded down
    to the nearest integer towards negative infinity. This is equivalent
    to ``x1 // x2`` in Python.

  Note:
    ``x1 // x2`` is equivalent to ``jnp.floor_divide(x1, x2)`` for arrays ``x1``
    and ``x2``

  See Also:
    :func:`jax.numpy.divide` and :func:`jax.numpy.true_divide` for floating point
    division.

  Examples:
    >>> x1 = jnp.array([10, 20, 30])
    >>> x2 = jnp.array([3, 4, 7])
    >>> jnp.floor_divide(x1, x2)
    Array([3, 5, 4], dtype=int32)

    >>> x1 = jnp.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
    >>> x2 = 3
    >>> jnp.floor_divide(x1, x2)
    Array([-2, -2, -1, -1, -1,  0,  0,  0,  1,  1,  1], dtype=int32)

    >>> x1 = jnp.array([6, 6, 6], dtype=jnp.int32)
    >>> x2 = jnp.array([2.0, 2.5, 3.0], dtype=jnp.float32)
    >>> jnp.floor_divide(x1, x2)
    Array([3., 2., 2.], dtype=float32)
  """
  x1, x2 = promote_args_numeric("floor_divide", x1, x2)
  dtype = dtypes.dtype(x1)
  if dtypes.issubdtype(dtype, np.unsignedinteger):
    return lax.div(x1, x2)
  elif dtypes.issubdtype(dtype, np.integer):
    quotient = lax.div(x1, x2)
    select = logical_and(lax.sign(x1) != lax.sign(x2), lax.rem(x1, x2) != 0)
    # TODO(mattjj): investigate why subtracting a scalar was causing promotion
    return _where(select, quotient - 1, quotient)
  elif dtypes.issubdtype(dtype, np.complexfloating):
    raise TypeError("floor_divide does not support complex-valued inputs")
  else:
    return _float_divmod(x1, x2)[0]
