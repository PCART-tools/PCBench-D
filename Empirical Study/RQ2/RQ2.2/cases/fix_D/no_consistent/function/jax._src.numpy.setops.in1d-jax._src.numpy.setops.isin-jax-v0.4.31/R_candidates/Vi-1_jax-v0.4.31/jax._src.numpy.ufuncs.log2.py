@partial(jit, inline=True)
def log2(x: ArrayLike, /) -> Array:
  """Calculates the base-2 logarithm of x element-wise

  LAX-backend implementation of :func:`numpy.log2`.

  Args:
    x: Input array

  Returns:
    An array containing the base-2 logarithm of each element in ``x``, promotes
    to inexact dtype.

  Examples:
    >>> x1 = jnp.array([0.25, 0.5, 1, 2, 4, 8])
    >>> jnp.log2(x1)
    Array([-2., -1.,  0.,  1.,  2.,  3.], dtype=float32)
  """
  x, = promote_args_inexact("log2", x)
  return lax.div(lax.log(x), lax.log(_constant_like(x, 2)))
