@jit
def copysign(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Copies the sign of each element in ``x2`` to the corresponding element in ``x1``.

  LAX-backend implementation of :func:`numpy.copysign`.

  Args:
    x1: Input array
    x2: The array whose elements will be used to determine the sign, must be
      broadcast-compatible with ``x1``

  Returns:
    An array object containing the potentially changed elements of ``x1``, always promotes
    to inexact dtype, and has a shape of ``jnp.broadcast_shapes(x1.shape, x2.shape)``

  Examples:
    >>> x1 = jnp.array([5, 2, 0])
    >>> x2 = -1
    >>> jnp.copysign(x1, x2)
    Array([-5., -2., -0.], dtype=float32)

    >>> x1 = jnp.array([6, 8, 0])
    >>> x2 = 2
    >>> jnp.copysign(x1, x2)
    Array([6., 8., 0.], dtype=float32)

    >>> x1 = jnp.array([2, -3])
    >>> x2 = jnp.array([[1],[-4], [5]])
    >>> jnp.copysign(x1, x2)
    Array([[ 2.,  3.],
           [-2., -3.],
           [ 2.,  3.]], dtype=float32)
  """
  x1, x2 = promote_args_inexact("copysign", x1, x2)
  if dtypes.issubdtype(dtypes.dtype(x1), np.complexfloating):
    raise TypeError("copysign does not support complex-valued inputs")
  return _where(signbit(x2).astype(bool), -lax.abs(x1), lax.abs(x1))
