@partial(jit, inline=True)
def _bitwise_xor(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Compute the bitwise XOR operation elementwise.

  JAX implementation of :obj:`numpy.bitwise_xor`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.

  Args:
    x, y: integer or boolean arrays. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise bitwise XOR.
  """
  return lax.bitwise_xor(*promote_args("bitwise_xor", x, y))
