@jax.jit
def soft_sign(x: Array) -> Array:
  r"""Soft-sign activation function.

  Computes the element-wise function

  .. math::
    \mathrm{soft\_sign}(x) = \frac{x}{|x| + 1}

  Args:
    x : input array
  """
  return x / (jnp.abs(x) + 1)
