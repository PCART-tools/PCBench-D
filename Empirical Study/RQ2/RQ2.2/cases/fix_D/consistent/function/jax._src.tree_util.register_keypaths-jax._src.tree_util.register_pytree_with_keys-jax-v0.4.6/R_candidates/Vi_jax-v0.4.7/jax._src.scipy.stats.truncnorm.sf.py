@_wraps(osp_stats.truncnorm.sf, update_doc=False)
def sf(x, a, b, loc=0, scale=1):
  return lax.exp(logsf(x, a, b, loc, scale))
