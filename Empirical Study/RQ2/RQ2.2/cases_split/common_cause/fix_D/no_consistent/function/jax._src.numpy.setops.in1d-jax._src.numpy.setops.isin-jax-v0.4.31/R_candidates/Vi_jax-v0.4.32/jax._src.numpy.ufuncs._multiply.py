@partial(jit, inline=True)
def _multiply(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Multiply two arrays element-wise.

  JAX implementation of :obj:`numpy.multiply`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.

  Args:
    x, y: arrays to multiply. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise multiplication.
  """
  x, y = promote_args("multiply", x, y)
  return lax.mul(x, y) if x.dtype != bool else lax.bitwise_and(x, y)
