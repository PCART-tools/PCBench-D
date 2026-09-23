@jax.jit
def hard_silu(x: Array) -> Array:
  r"""Hard SiLU activation function

  Computes the element-wise function

  .. math::
    \mathrm{hard\_silu}(x) = x \cdot \mathrm{hard\_sigmoid}(x)

  Args:
    x : input array
  """
  return x * hard_sigmoid(x)
