@partial(jit, inline=True)
def _bitwise_or(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Compute the bitwise OR operation elementwise.

  JAX implementation of :obj:`numpy.bitwise_or`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.

  Args:
    x, y: integer or boolean arrays. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise bitwise OR.
  """
  return lax.bitwise_or(*promote_args("bitwise_or", x, y))
