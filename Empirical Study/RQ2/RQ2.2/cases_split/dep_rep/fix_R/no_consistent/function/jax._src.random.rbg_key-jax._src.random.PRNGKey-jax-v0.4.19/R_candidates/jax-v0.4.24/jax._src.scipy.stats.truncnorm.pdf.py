@implements(osp_stats.truncnorm.pdf, update_doc=False)
def pdf(x, a, b, loc=0, scale=1):
  return lax.exp(logpdf(x, a, b, loc, scale))
