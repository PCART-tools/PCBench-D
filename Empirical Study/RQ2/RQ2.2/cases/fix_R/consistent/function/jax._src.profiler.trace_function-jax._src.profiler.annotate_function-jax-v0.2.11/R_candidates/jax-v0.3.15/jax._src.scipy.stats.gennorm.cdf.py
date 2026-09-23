@_wraps(osp_stats.gennorm.cdf, update_doc=False)
def cdf(x, p):
  x, p = _promote_args_inexact("gennorm.cdf", x, p)
  return .5 * (1 + lax.sign(x) * lax.igamma(1/p, lax.abs(x)**p))
