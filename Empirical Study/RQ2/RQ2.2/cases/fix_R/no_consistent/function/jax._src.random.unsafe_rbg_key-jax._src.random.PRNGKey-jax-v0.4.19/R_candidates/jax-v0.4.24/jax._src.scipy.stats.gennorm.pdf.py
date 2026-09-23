@implements(osp_stats.gennorm.pdf, update_doc=False)
def pdf(x: ArrayLike, p: ArrayLike) -> Array:
  return lax.exp(logpdf(x, p))
