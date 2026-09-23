@_wraps(osp_stats.norm.ppf, update_doc=False)
def ppf(q, loc=0, scale=1):
  return jnp.asarray(special.ndtri(q) * scale + loc, float)
