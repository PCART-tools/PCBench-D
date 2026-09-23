@_wraps(osp_stats.truncnorm.cdf, update_doc=False)
def cdf(x, a, b, loc=0, scale=1):
  return lax.exp(logcdf(x, a, b, loc, scale))
