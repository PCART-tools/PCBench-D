@partial(jit, inline=True)
def _logical_and(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Compute the logical AND operation elementwise.

  JAX implementation of :obj:`numpy.logical_and`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.

  Args:
    x, y: input arrays. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise logical AND.
  """
  return lax.bitwise_and(*map(_to_bool, promote_args("logical_and", x, y)))
