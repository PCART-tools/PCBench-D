@implements(osp_stats.vonmises.pdf, update_doc=False)
def pdf(x: ArrayLike, kappa: ArrayLike) -> Array:
  return lax.exp(logpdf(x, kappa))
