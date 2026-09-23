def clamp(min: Array, x: Array, max: Array) -> Array:
  r"""Elementwise clamp.

  Returns :math:`\mathrm{clamp}(x) = \begin{cases}
  \mathit{min} & \text{if } x < \mathit{min},\\
  \mathit{max} & \text{if } x > \mathit{max},\\
  x & \text{otherwise}
  \end{cases}`.
  """
  return clamp_p.bind(min, x, max)
