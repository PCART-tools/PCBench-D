@jax.jit
def elu(x: Array, alpha: Array = 1.0) -> Array:
  r"""Exponential linear unit activation function.

  Computes the element-wise function:

  .. math::
    \mathrm{elu}(x) = \begin{cases}
      x, & x > 0\\
      \alpha \left(\exp(x) - 1\right), & x \le 0
    \end{cases}

  Args:
    x : input array
    alpha : scalar or array of alpha values (default: 1.0)

  Returns:
    An array.

  See also:
    :func:`selu`
  """
  safe_x = jnp.where(x > 0, 0., x)
  return jnp.where(x > 0, x, alpha * jnp.expm1(safe_x))
