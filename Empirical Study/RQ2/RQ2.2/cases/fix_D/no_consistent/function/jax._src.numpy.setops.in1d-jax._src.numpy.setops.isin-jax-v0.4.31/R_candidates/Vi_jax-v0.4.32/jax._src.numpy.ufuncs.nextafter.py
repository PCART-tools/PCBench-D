@partial(jit, inline=True)
def nextafter(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Return element-wise next floating point value after ``x`` towards ``y``.

  JAX implementation of :obj:`numpy.nextafter`.

  Args:
    x: scalar or array. Specifies the value after which the next number is found.
    y: scalar or array. Specifies the direction towards which the next number is
      found. ``x`` and ``y`` should either have same shape or be broadcast
      compatible.

  Returns:
    An array containing the next representable number of ``x`` in the direction
    of ``y``.

  Examples:
    >>> jnp.nextafter(2, 1)  # doctest: +SKIP
    Array(1.9999999, dtype=float32, weak_type=True)
    >>> x = jnp.array([3, -2, 1])
    >>> y = jnp.array([2, -1, 2])
    >>> jnp.nextafter(x, y)  # doctest: +SKIP
    Array([ 2.9999998, -1.9999999,  1.0000001], dtype=float32)
  """
  return lax.nextafter(*promote_args_inexact("nextafter", x, y))
