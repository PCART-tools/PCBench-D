@_wraps(osp_stats.bernoulli.pmf, update_doc=False)
def pmf(k, p, loc=0):
  return jnp.exp(logpmf(k, p, loc))
