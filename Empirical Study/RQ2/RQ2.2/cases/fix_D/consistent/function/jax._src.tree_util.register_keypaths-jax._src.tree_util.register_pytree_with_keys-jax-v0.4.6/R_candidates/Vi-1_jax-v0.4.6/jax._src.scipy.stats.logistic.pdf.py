@_wraps(osp_stats.logistic.pdf, update_doc=False)
def pdf(x: ArrayLike) -> Array:
  return lax.exp(logpdf(x))
