@implements(osp_stats.norm.logsf, update_doc=False)
def logsf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, loc, scale = promote_args_inexact("norm.logsf", x, loc, scale)
  return logcdf(-x, -loc, scale)
