@_wraps(osp_stats.logistic.cdf, update_doc=False)
def cdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, loc, scale = promote_args_inexact("logistic.cdf", x, loc, scale)
  return expit(lax.div(lax.sub(x, loc), scale))
