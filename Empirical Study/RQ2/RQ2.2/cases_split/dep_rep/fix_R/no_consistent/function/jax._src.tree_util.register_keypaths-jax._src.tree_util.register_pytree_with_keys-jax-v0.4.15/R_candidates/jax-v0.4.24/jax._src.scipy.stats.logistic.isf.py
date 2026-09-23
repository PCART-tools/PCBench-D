@implements(osp_stats.logistic.isf, update_doc=False)
def isf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, loc, scale = promote_args_inexact("logistic.isf", x, loc, scale)
  return lax.add(lax.mul(lax.neg(logit(x)), scale), loc)
