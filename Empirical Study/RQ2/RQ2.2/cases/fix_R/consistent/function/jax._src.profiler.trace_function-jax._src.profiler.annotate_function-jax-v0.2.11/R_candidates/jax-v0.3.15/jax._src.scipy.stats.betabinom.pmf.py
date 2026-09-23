def pmf(k, n, a, b, loc=0):
  """JAX implementation of scipy.stats.betabinom.pmf."""
  return lax.exp(logpmf(k, n, a, b, loc))
