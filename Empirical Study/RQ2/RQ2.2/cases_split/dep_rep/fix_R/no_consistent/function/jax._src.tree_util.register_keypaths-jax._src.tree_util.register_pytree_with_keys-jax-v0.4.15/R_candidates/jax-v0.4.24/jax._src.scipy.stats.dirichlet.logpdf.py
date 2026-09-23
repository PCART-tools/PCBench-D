@implements(osp_stats.dirichlet.logpdf, update_doc=False)
def logpdf(x: ArrayLike, alpha: ArrayLike) -> Array:
  return _logpdf(*promote_dtypes_inexact(x, alpha))
