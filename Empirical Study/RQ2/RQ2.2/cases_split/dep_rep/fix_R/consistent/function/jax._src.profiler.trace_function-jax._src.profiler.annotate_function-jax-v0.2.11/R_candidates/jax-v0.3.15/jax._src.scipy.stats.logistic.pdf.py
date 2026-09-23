@_wraps(osp_stats.logistic.pdf, update_doc=False)
def pdf(x):
  return lax.exp(logpdf(x))
