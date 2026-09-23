@_wraps(osp_stats.chi2.logcdf, update_doc=False)
def logcdf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  return lax.log(cdf(x, df, loc, scale))
