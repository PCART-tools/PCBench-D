@implements(osp_stats.norm.sf, update_doc=False)
def sf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, loc, scale = promote_args_inexact("norm.sf", x, loc, scale)
  return cdf(-x, -loc, scale)
