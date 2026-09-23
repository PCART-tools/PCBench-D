@custom_jvp
@jax.jit
def relu(x: Array) -> Array:
  r"""Rectified linear unit activation function.

  Computes the element-wise function:

  .. math::
    \mathrm{relu}(x) = \max(x, 0)

  Args:
    x : input array
  """
  return jnp.maximum(x, 0)
