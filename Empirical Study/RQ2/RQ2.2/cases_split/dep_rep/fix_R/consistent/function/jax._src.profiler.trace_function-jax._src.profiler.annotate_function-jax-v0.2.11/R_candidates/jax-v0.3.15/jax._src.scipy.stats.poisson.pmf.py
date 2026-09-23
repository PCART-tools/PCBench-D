@_wraps(osp_stats.poisson.pmf, update_doc=False)
def pmf(k, mu, loc=0):
  return jnp.exp(logpmf(k, mu, loc))
