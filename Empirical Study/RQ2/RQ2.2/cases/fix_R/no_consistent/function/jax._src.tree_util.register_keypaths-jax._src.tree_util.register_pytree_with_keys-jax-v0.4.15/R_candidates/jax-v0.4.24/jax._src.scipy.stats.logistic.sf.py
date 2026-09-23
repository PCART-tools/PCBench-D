@implements(osp_stats.logistic.sf, update_doc=False)
def sf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, loc, scale = promote_args_inexact("logistic.sf", x, loc, scale)
  return expit(lax.neg(lax.div(lax.sub(x, loc), scale)))
