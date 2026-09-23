@_wraps(osp_stats.dirichlet.pdf, update_doc=False)
def pdf(x, alpha):
  return lax.exp(logpdf(x, alpha))
