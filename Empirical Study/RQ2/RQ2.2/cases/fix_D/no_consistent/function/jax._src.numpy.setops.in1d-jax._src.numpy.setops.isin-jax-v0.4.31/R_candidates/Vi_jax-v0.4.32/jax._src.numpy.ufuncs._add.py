@partial(jit, inline=True)
def _add(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Add two arrays element-wise.

  JAX implementation of :obj:`numpy.add`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.

  Args:
    x, y: arrays to add. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise addition.
  """
  x, y = promote_args("add", x, y)
  return lax.add(x, y) if x.dtype != bool else lax.bitwise_or(x, y)
