@_wraps(osp_stats.cauchy.logcdf, update_doc=False)
def logcdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  return lax.log(cdf(x, loc, scale))
