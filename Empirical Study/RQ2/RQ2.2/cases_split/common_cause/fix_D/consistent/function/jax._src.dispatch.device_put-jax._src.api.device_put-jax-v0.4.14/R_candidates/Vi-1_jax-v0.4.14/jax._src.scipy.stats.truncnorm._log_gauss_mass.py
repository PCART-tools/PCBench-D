def _log_gauss_mass(a, b):
  """Log of Gaussian probability mass within an interval"""
  a, b = jnp.array(a), jnp.array(b)
  a, b = jnp.broadcast_arrays(a, b)

  # Note: Docstring carried over from scipy
  # Calculations in right tail are inaccurate, so we'll exploit the
  # symmetry and work only in the left tail
  case_left = b <= 0
  case_right = a > 0
  case_central = ~(case_left | case_right)

  def mass_case_left(a, b):
    return _log_diff(log_ndtr(b), log_ndtr(a))

  def mass_case_right(a, b):
    return mass_case_left(-b, -a)

  def mass_case_central(a, b):
    # Note: Docstring carried over from scipy
    # Previously, this was implemented as:
    # left_mass = mass_case_left(a, 0)
    # right_mass = mass_case_right(0, b)
    # return _log_sum(left_mass, right_mass)
    # Catastrophic cancellation occurs as np.exp(log_mass) approaches 1.
    # Correct for this with an alternative formulation.
    # We're not concerned with underflow here: if only one term
    # underflows, it was insignificant; if both terms underflow,
    # the result can't accurately be represented in logspace anyway
    # because sc.log1p(x) ~ x for small x.
    return jnp.log1p(-ndtr(a) - ndtr(-b))

  out = jnp.select(
    [case_left, case_right, case_central],
    [mass_case_left(a, b), mass_case_right(a, b), mass_case_central(a, b)]
  )
  return out
