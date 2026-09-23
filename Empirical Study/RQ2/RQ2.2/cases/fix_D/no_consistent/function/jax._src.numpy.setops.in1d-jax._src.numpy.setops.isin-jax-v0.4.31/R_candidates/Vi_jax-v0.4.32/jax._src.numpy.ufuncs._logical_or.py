@partial(jit, inline=True)
def _logical_or(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Compute the logical OR operation elementwise.

  JAX implementation of :obj:`numpy.logical_or`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.

  Args:
    x, y: input arrays. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise logical OR.
  """
  return lax.bitwise_or(*map(_to_bool, promote_args("logical_or", x, y)))
