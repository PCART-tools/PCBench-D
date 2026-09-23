@jax.jit
def softplus(x: Array) -> Array:
  r"""Softplus activation function.

  Computes the element-wise function

  .. math::
    \mathrm{softplus}(x) = \log(1 + e^x)

  Args:
    x : input array
  """
  return jnp.logaddexp(x, 0)
