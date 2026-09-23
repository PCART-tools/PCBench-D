@_wraps(osp_stats.gennorm.pdf, update_doc=False)
def pdf(x, p):
  return lax.exp(logpdf(x, p))
