@_wraps(osp_stats.pareto.pdf, update_doc=False)
def pdf(x: ArrayLike, b: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  return lax.exp(logpdf(x, b, loc, scale))
