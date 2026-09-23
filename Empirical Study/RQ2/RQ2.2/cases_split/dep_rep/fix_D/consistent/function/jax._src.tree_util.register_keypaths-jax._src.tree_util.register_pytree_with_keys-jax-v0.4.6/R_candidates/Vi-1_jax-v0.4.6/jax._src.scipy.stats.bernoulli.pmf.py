@_wraps(osp_stats.bernoulli.pmf, update_doc=False)
def pmf(k: ArrayLike, p: ArrayLike, loc: ArrayLike = 0) -> Array:
  return jnp.exp(logpmf(k, p, loc))
