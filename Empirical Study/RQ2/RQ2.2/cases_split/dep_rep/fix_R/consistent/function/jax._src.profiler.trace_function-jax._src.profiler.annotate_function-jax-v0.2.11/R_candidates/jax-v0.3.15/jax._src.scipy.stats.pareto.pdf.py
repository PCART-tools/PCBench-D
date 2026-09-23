@_wraps(osp_stats.pareto.pdf, update_doc=False)
def pdf(x, b, loc=0, scale=1):
  return lax.exp(logpdf(x, b, loc, scale))
