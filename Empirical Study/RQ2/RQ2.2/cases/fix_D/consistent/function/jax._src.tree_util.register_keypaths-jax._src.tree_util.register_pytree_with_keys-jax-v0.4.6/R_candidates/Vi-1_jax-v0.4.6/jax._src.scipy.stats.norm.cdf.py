@_wraps(osp_stats.norm.cdf, update_doc=False)
def cdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, loc, scale = _promote_args_inexact("norm.cdf", x, loc, scale)
  return special.ndtr(lax.div(lax.sub(x, loc), scale))
