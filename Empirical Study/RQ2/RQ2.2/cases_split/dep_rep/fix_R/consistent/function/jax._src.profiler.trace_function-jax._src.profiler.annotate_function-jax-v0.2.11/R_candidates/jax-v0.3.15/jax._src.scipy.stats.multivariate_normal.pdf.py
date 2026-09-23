@_wraps(osp_stats.multivariate_normal.pdf, update_doc=False)
def pdf(x, mean, cov):
  return lax.exp(logpdf(x, mean, cov))
