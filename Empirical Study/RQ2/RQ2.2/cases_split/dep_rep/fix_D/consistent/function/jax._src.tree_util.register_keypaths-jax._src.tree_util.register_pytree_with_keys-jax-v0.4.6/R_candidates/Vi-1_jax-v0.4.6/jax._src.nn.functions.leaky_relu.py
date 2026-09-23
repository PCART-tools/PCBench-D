@jax.jit
def leaky_relu(x: Array, negative_slope: Array = 1e-2) -> Array:
  r"""Leaky rectified linear unit activation function.

  Computes the element-wise function:

  .. math::
    \mathrm{leaky\_relu}(x) = \begin{cases}
      x, & x \ge 0\\
      \alpha x, & x < 0
    \end{cases}

  where :math:`\alpha` = :code:`negative_slope`.

  Args:
    x : input array
    negative_slope : array or scalar specifying the negative slope (default: 0.01)
  """
  return jnp.where(x >= 0, x, negative_slope * x)
