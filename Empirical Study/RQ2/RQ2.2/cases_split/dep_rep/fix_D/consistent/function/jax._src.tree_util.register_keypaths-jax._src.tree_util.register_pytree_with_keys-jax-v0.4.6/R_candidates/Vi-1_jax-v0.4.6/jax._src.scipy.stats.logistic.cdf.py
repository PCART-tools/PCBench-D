@_wraps(osp_stats.logistic.cdf, update_doc=False)
def cdf(x):
  return expit(x)
