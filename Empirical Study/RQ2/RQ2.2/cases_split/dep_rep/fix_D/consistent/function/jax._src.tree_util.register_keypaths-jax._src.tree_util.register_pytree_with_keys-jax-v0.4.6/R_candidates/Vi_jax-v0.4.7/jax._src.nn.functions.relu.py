@custom_jvp
@jax.jit
def relu(x: Array) -> Array:
  r"""Rectified linear unit activation function.

  Computes the element-wise function:

  .. math::
    \mathrm{relu}(x) = \max(x, 0)

  except under differentiation, we take:

  .. math::
    \nabla \mathrm{relu}(0) = 0

  For more information see
  `Numerical influence of ReLU’(0) on backpropagation
  <https://openreview.net/forum?id=urrcVI-_jRm>`_.

  Args:
    x : input array
  """
  return jnp.maximum(x, 0)
