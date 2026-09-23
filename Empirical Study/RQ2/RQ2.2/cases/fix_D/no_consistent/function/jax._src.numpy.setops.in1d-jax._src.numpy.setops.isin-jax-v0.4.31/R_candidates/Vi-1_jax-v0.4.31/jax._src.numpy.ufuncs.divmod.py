@jit
def divmod(x1: ArrayLike, x2: ArrayLike, /) -> tuple[Array, Array]:
  """Calculates the integer quotient and remainder of x1 by x2 element-wise

  LAX-backend implementation of :func:`numpy.divmod`.

  Args:
    x1: Input array, the dividend
    x2: Input array, the divisor

  Returns:
    A tuple of arrays ``(x1 // x2, x1 % x2)``.

  Examples:
    >>> x1 = jnp.array([10, 20, 30])
    >>> x2 = jnp.array([3, 4, 7])
    >>> jnp.divmod(x1, x2)
    (Array([3, 5, 4], dtype=int32), Array([1, 0, 2], dtype=int32))

    >>> x1 = jnp.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
    >>> x2 = 3
    >>> jnp.divmod(x1, x2)
    (Array([-2, -2, -1, -1, -1,  0,  0,  0,  1,  1,  1], dtype=int32),
     Array([1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2], dtype=int32))

    >>> x1 = jnp.array([6, 6, 6], dtype=jnp.int32)
    >>> x2 = jnp.array([1.9, 2.5, 3.1], dtype=jnp.float32)
    >>> jnp.divmod(x1, x2)
    (Array([3., 2., 1.], dtype=float32),
     Array([0.30000007, 1.        , 2.9       ], dtype=float32))

  See Also:
    - :func:`jax.numpy.floor_divide`: floor division function
    - :func:`jax.numpy.remainder`: remainder function
  """
  x1, x2 = promote_args_numeric("divmod", x1, x2)
  if dtypes.issubdtype(dtypes.dtype(x1), np.integer):
    return floor_divide(x1, x2), remainder(x1, x2)
  else:
    return _float_divmod(x1, x2)
