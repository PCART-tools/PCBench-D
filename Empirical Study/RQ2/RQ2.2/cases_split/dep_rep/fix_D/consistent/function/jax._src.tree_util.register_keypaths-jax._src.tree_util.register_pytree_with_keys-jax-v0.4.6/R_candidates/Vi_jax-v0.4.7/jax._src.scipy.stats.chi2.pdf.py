@_wraps(osp_stats.chi2.pdf, update_doc=False)
def pdf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  return lax.exp(logpdf(x, df, loc, scale))
