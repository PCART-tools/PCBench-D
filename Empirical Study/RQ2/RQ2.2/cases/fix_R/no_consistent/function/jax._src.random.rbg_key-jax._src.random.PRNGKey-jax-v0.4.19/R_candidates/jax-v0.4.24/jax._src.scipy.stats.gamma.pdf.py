@implements(osp_stats.gamma.pdf, update_doc=False)
def pdf(x: ArrayLike, a: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  return lax.exp(logpdf(x, a, loc, scale))
