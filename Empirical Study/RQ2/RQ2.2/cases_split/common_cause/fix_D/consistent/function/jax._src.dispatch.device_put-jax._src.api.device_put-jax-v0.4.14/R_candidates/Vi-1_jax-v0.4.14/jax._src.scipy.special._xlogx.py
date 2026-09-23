@custom_derivatives.custom_jvp
def _xlogx(x):
  """Compute x log(x) with well-defined derivatives."""
  return xlogy(x, x)
