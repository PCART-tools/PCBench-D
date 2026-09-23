@implements(osp_stats.logistic.ppf, update_doc=False)
def ppf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, loc, scale = promote_args_inexact("logistic.ppf", x, loc, scale)
  return lax.add(lax.mul(logit(x), scale), loc)
