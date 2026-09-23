@jax.jit
def silu(x: Array) -> Array:
  r"""SiLU activation function.

  Computes the element-wise function:

  .. math::
    \mathrm{silu}(x) = x \cdot \mathrm{sigmoid}(x) = \frac{x}{1 + e^{-x}}

  Args:
    x : input array
  """
  return x * sigmoid(x)
