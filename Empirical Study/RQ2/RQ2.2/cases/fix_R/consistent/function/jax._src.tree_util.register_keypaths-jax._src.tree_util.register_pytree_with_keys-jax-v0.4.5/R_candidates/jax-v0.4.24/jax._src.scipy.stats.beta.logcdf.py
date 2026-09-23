@implements(osp_stats.beta.logcdf, update_doc=False)
def logcdf(x: ArrayLike, a: ArrayLike, b: ArrayLike,
           loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  return lax.log(cdf(x, a, b, loc, scale))
