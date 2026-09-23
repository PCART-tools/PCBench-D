@_wraps(osp_stats.norm.cdf, update_doc=False)
def cdf(x, loc=0, scale=1):
  x, loc, scale = _promote_args_inexact("norm.cdf", x, loc, scale)
  return special.ndtr(lax.div(lax.sub(x, loc), scale))
