@partial(jit, inline=True)
def exp(x: ArrayLike, /) -> Array:
  """Calculate element-wise exponential of the input.

  JAX implementation of :obj:`numpy.exp`.

  Args:
    x: input array or scalar

  Returns:
    An array containing the exponential of each element in ``x``, promotes to
    inexact dtype.

  See also:
    - :func:`jax.numpy.log`: Calculates element-wise logarithm of the input.
    - :func:`jax.numpy.expm1`: Calculates :math:`e^x-1` of each element of the
      input.
    - :func:`jax.numpy.exp2`: Calculates base-2 exponential of each element of
      the input.

  Examples:
    ``jnp.exp`` follows the properties of exponential such as :math:`e^{(a+b)}
    = e^a * e^b`.

    >>> x1 = jnp.array([2, 4, 3, 1])
    >>> x2 = jnp.array([1, 3, 2, 3])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.exp(x1+x2))
    [  20.09 1096.63  148.41   54.6 ]
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.exp(x1)*jnp.exp(x2))
    [  20.09 1096.63  148.41   54.6 ]

    This property holds for complex input also:

    >>> jnp.allclose(jnp.exp(3-4j), jnp.exp(3)*jnp.exp(-4j))
    Array(True, dtype=bool)
  """
  return lax.exp(*promote_args_inexact('exp', x))
