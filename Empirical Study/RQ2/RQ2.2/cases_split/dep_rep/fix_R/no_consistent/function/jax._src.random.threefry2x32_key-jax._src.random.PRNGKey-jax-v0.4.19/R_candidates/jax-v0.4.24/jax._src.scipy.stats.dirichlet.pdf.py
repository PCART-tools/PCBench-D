@implements(osp_stats.dirichlet.pdf, update_doc=False)
def pdf(x: ArrayLike, alpha: ArrayLike) -> Array:
  return lax.exp(logpdf(x, alpha))
