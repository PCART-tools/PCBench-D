@implements(osp_stats.wrapcauchy.pdf, update_doc=False)
def pdf(x: ArrayLike, c: ArrayLike) -> Array:
  return lax.exp(logpdf(x, c))
