@implements(osp_stats.poisson.pmf, update_doc=False)
def pmf(k: ArrayLike, mu: ArrayLike, loc: ArrayLike = 0) -> Array:
  return jnp.exp(logpmf(k, mu, loc))
