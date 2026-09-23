@partial(jit, inline=True)
def _logical_xor(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Compute the logical XOR operation elementwise.

  JAX implementation of :obj:`numpy.logical_xor`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.

  Args:
    x, y: input arrays. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise logical XOR.
  """
  return lax.bitwise_xor(*map(_to_bool, promote_args("logical_xor", x, y)))
