def gelu(x: Array, approximate: bool = True) -> Array:
  r"""Gaussian error linear unit activation function.

  If ``approximate=False``, computes the element-wise function:

  .. math::
    \mathrm{gelu}(x) = \frac{x}{2} \left(1 + \mathrm{erf} \left(
      \frac{x}{\sqrt{2}} \right) \right)

  If ``approximate=True``, uses the approximate formulation of GELU:

  .. math::
    \mathrm{gelu}(x) = \frac{x}{2} \left(1 + \mathrm{tanh} \left(
      \sqrt{\frac{2}{\pi}} \left(x + 0.044715 x^3 \right) \right) \right)

  For more information, see `Gaussian Error Linear Units (GELUs)
  <https://arxiv.org/abs/1606.08415>`_, section 2.

  Args:
    x : input array
    approximate: whether to use the approximate or exact formulation.
  """
  if approximate:
    sqrt_2_over_pi = np.sqrt(2 / np.pi).astype(x.dtype)
    cdf = 0.5 * (1.0 + jnp.tanh(sqrt_2_over_pi * (x + 0.044715 * (x ** 3))))
    return x * cdf
  else:
    sqrt_2 = np.sqrt(2).astype(x.dtype)
    return jnp.array(x * (lax.erf(x / sqrt_2) + 1) / 2, dtype=x.dtype)
