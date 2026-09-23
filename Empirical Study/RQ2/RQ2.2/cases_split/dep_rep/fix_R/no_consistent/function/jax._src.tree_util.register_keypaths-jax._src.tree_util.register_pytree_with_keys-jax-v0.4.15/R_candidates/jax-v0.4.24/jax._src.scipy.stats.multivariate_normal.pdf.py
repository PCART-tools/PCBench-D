@implements(osp_stats.multivariate_normal.pdf, update_doc=False)
def pdf(x: ArrayLike, mean: ArrayLike, cov: ArrayLike) -> Array:
  return lax.exp(logpdf(x, mean, cov))
