@partial(jit, inline=True)
def expm1(x: ArrayLike, /) -> Array:
  """Calculate ``exp(x)-1`` of each element of the input.

  JAX implementation of :obj:`numpy.expm1`.

  Args:
    x: input array or scalar.

  Returns:
    An array containing ``exp(x)-1`` of each element in ``x``, promotes to inexact
    dtype.

  Note:
    ``jnp.expm1`` has much higher precision than the naive computation of
    ``exp(x)-1`` for small values of ``x``.

  See also:
    - :func:`jax.numpy.log1p`: Calculates element-wise logarithm of one plus input.
    - :func:`jax.numpy.exp`: Calculates element-wise exponential of the input.
    - :func:`jax.numpy.exp2`: Calculates base-2 exponential of each element of
      the input.

  Examples:
    >>> x = jnp.array([2, -4, 3, -1])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.expm1(x))
    [ 6.39 -0.98 19.09 -0.63]
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.exp(x)-1)
    [ 6.39 -0.98 19.09 -0.63]

    For values very close to 0, ``jnp.expm1(x)`` is much more accurate than
    ``jnp.exp(x)-1``:

    >>> x1 = jnp.array([1e-4, 1e-6, 2e-10])
    >>> jnp.expm1(x1)
    Array([1.0000500e-04, 1.0000005e-06, 2.0000000e-10], dtype=float32)
    >>> jnp.exp(x1)-1
    Array([1.00016594e-04, 9.53674316e-07, 0.00000000e+00], dtype=float32)
  """
  return lax.expm1(*promote_args_inexact('expm1', x))
