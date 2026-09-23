@implements(osp_stats.betabinom.pmf, update_doc=False)
def pmf(k: ArrayLike, n: ArrayLike, a: ArrayLike, b: ArrayLike,
        loc: ArrayLike = 0) -> Array:
  """JAX implementation of scipy.stats.betabinom.pmf."""
  return lax.exp(logpmf(k, n, a, b, loc))
