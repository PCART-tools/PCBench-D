@_wraps(osp_stats.gamma.logcdf, update_doc=False)
def logcdf(x: ArrayLike, a: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  return lax.log(cdf(x, a, loc, scale))
