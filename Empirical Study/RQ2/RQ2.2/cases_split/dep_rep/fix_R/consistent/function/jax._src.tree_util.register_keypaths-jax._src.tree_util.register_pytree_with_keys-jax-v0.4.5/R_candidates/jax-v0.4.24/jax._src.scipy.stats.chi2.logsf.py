@implements(osp_stats.chi2.logsf, update_doc=False)
def logsf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  return lax.log(sf(x, df, loc, scale))
