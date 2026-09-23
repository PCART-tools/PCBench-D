@partial(jit, inline=True)
def log10(x: ArrayLike, /) -> Array:
  """Calculates the base-10 logarithm of x element-wise

  LAX-backend implementation of :func:`numpy.log10`.

  Args:
    x: Input array

  Returns:
    An array containing the base-10 logarithm of each element in ``x``, promotes
    to inexact dtype.

  Examples:
    >>> x1 = jnp.array([0.01, 0.1, 1, 10, 100, 1000])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.log10(x1))
    [-2. -1.  0.  1.  2.  3.]
  """
  x, = promote_args_inexact("log10", x)
  return lax.div(lax.log(x), lax.log(_constant_like(x, 10)))
