@partial(jit, inline=True)
def _bitwise_and(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Compute the bitwise AND operation elementwise.

  JAX implementation of :obj:`numpy.bitwise_and`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.

  Args:
    x, y: integer or boolean arrays. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise bitwise AND.
  """
  return lax.bitwise_and(*promote_args("bitwise_and", x, y))
