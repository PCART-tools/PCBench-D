@implements(osp_stats.multinomial.pmf, update_doc=False)
def pmf(x: ArrayLike, n: ArrayLike, p: ArrayLike) -> Array:
  """JAX implementation of scipy.stats.multinomial.pmf."""
  return lax.exp(logpmf(x, n, p))
