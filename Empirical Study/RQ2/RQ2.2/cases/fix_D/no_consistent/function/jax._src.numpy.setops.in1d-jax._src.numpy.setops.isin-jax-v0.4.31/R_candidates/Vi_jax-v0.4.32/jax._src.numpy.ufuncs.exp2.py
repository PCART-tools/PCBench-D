@partial(jit, inline=True)
def exp2(x: ArrayLike, /) -> Array:
  """Calculate element-wise base-2 exponential of input.

  JAX implementation of :obj:`numpy.exp2`.

  Args:
    x: input array or scalar

  Returns:
    An array containing the base-2 exponential of each element in ``x``, promotes
    to inexact dtype.

  See also:
    - :func:`jax.numpy.log2`: Calculates base-2 logarithm of each element of input.
    - :func:`jax.numpy.exp`: Calculates exponential of each element of the input.
    - :func:`jax.numpy.expm1`: Calculates :math:`e^x-1` of each element of the
      input.

  Examples:
    ``jnp.exp2`` follows the properties of the exponential such as :math:`2^{a+b}
    = 2^a * 2^b`.

    >>> x1 = jnp.array([2, -4, 3, -1])
    >>> x2 = jnp.array([-1, 3, -2, 3])
    >>> jnp.exp2(x1+x2)
    Array([2. , 0.5, 2. , 4. ], dtype=float32)
    >>> jnp.exp2(x1)*jnp.exp2(x2)
    Array([2. , 0.5, 2. , 4. ], dtype=float32)
  """
  x, = promote_args_inexact("exp2", x)
  return lax.exp2(x)
