@jax.jit
def hard_sigmoid(x: Array) -> Array:
  r"""Hard Sigmoid activation function.

  Computes the element-wise function

  .. math::
    \mathrm{hard\_sigmoid}(x) = \frac{\mathrm{relu6}(x + 3)}{6}

  Args:
    x : input array
  """
  return relu6(x + 3.) / 6.
