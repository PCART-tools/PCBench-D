@_wraps(osp_stats.t.pdf, update_doc=False)
def pdf(x, df, loc=0, scale=1):
  return lax.exp(logpdf(x, df, loc, scale))
