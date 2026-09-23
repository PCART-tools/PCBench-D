@_wraps(osp_stats.gamma.pdf, update_doc=False)
def pdf(x, a, loc=0, scale=1):
  return lax.exp(logpdf(x, a, loc, scale))
