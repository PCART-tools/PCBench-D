@jax.jit
def sigmoid(x: Array) -> Array:
  r"""Sigmoid activation function.

  Computes the element-wise function:

  .. math::
    \mathrm{sigmoid}(x) = \frac{1}{1 + e^{-x}}

  Args:
    x : input array
  """
  return expit(x)
