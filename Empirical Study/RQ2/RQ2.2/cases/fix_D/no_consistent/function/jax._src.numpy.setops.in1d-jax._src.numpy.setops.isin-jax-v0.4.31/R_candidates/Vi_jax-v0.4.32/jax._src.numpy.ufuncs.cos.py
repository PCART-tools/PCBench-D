@partial(jit, inline=True)
def cos(x: ArrayLike, /) -> Array:
  """Compute a trigonometric cosine of each element of input.

  JAX implementation of :obj:`numpy.cos`.

  Args:
    x: scalar or array. Angle in radians.

  Returns:
    An array containing the cosine of each element in ``x``, promotes to inexact
    dtype.

  See also:
    - :func:`jax.numpy.sin`: Computes a trigonometric sine of each element of input.
    - :func:`jax.numpy.tan`: Computes a trigonometric tangent of each element of
      input.
    - :func:`jax.numpy.arccos` and :func:`jax.numpy.acos`: Computes the inverse of
      trigonometric cosine of each element of input.

  Examples:
    >>> pi = jnp.pi
    >>> x = jnp.array([pi/4, pi/2, 3*pi/4, 5*pi/6])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   print(jnp.cos(x))
    [ 0.707 -0.    -0.707 -0.866]
  """
  return lax.cos(*promote_args_inexact('cos', x))
