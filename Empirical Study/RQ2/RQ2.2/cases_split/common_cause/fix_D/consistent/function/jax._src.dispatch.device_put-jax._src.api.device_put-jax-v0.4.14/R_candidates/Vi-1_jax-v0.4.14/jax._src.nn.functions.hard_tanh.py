@jax.jit
def hard_tanh(x: Array) -> Array:
  r"""Hard :math:`\mathrm{tanh}` activation function.

  Computes the element-wise function:

  .. math::
    \mathrm{hard\_tanh}(x) = \begin{cases}
      -1, & x < -1\\
      x, & -1 \le x \le 1\\
      1, & 1 < x
    \end{cases}

  Args:
    x : input array
  """
  return jnp.where(x > 1, 1, jnp.where(x < -1, -1, x))
