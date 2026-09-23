@partial(jit, inline=True)
def true_divide(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Calculates the division of x1 by x2 element-wise

  JAX implementation of :func:`numpy.true_divide`.

  Args:
    x1: Input array, the dividend
    x2: Input array, the divisor

  Returns:
    An array containing the elementwise quotients, will always use
    floating point division.

  Examples:
    >>> x1 = jnp.array([3, 4, 5])
    >>> x2 = 2
    >>> jnp.true_divide(x1, x2)
    Array([1.5, 2. , 2.5], dtype=float32)

    >>> x1 = 24
    >>> x2 = jnp.array([3, 4, 6j])
    >>> jnp.true_divide(x1, x2)
    Array([8.+0.j, 6.+0.j, 0.-4.j], dtype=complex64)

    >>> x1 = jnp.array([1j, 9+5j, -4+2j])
    >>> x2 = 3j
    >>> jnp.true_divide(x1, x2)
    Array([0.33333334+0.j       , 1.6666666 -3.j       ,
           0.6666667 +1.3333334j], dtype=complex64)

  See Also:
    :func:`jax.numpy.floor_divide` for integer division
  """
  x1, x2 = promote_args_inexact("true_divide", x1, x2)
  return lax.div(x1, x2)
