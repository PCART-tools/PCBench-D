@partial(jit, inline=True)
def sin(x: ArrayLike, /) -> Array:
  """Compute a trigonometric sine of each element of input.

  JAX implementation of :obj:`numpy.sin`.

  Args:
    x: array or scalar. Angle in radians.

  Returns:
    An array containing the sine of each element in ``x``, promotes to inexact
    dtype.

  See also:
    - :func:`jax.numpy.cos`: Computes a trigonometric cosine of each element of
      input.
    - :func:`jax.numpy.tan`: Computes a trigonometric tangent of each element of
      input.
    - :func:`jax.numpy.arcsin` and :func:`jax.numpy.asin`: Computes the inverse of
      trigonometric sine of each element of input.

  Examples:
    >>> pi = jnp.pi
    >>> x = jnp.array([pi/4, pi/2, 3*pi/4, pi])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   print(jnp.sin(x))
    [ 0.707  1.     0.707 -0.   ]
  """
  return lax.sin(*promote_args_inexact('sin', x))
