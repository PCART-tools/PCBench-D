@_wraps(osp_stats.geom.pmf, update_doc=False)
def pmf(k, p, loc=0):
  return jnp.exp(logpmf(k, p, loc))
