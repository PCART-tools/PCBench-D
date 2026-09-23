@jax.jit
def relu6(x: Array) -> Array:
  r"""Rectified Linear Unit 6 activation function.

  Computes the element-wise function

  .. math::
    \mathrm{relu6}(x) = \min(\max(x, 0), 6)

  Args:
    x : input array
  """
  return jnp.minimum(jnp.maximum(x, 0), 6.)
