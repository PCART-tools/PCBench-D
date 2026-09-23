@implements(osp_stats.gennorm.logpdf, update_doc=False)
def logpdf(x: ArrayLike, p: ArrayLike) -> Array:
  x, p = promote_args_inexact("gennorm.logpdf", x, p)
  return lax.log(.5 * p) - lax.lgamma(1/p) - lax.abs(x)**p
