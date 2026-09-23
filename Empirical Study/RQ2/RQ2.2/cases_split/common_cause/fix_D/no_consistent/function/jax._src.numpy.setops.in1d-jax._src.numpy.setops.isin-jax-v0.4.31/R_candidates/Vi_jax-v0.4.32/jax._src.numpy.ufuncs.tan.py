@partial(jit, inline=True)
def tan(x: ArrayLike, /) -> Array:
  """Compute a trigonometric tangent of each element of input.

  JAX implementation of :obj:`numpy.tan`.

  Args:
    x: scalar or array. Angle in radians.

  Returns:
    An array containing the tangent of each element in ``x``, promotes to inexact
    dtype.

  See also:
    - :func:`jax.numpy.sin`: Computes a trigonometric sine of each element of input.
    - :func:`jax.numpy.cos`: Computes a trigonometric cosine of each element of
      input.
    - :func:`jax.numpy.arctan` and :func:`jax.numpy.atan`: Computes the inverse of
      trigonometric tangent of each element of input.

  Examples:
    >>> pi = jnp.pi
    >>> x = jnp.array([0, pi/6, pi/4, 3*pi/4, 5*pi/6])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   print(jnp.tan(x))
    [ 0.     0.577  1.    -1.    -0.577]
  """
  return lax.tan(*promote_args_inexact('tan', x))
