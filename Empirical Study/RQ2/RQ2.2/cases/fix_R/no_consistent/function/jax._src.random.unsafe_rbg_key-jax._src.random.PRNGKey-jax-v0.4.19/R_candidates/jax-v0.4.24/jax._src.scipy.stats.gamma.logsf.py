@implements(osp_stats.gamma.logsf, update_doc=False)
def logsf(x: ArrayLike, a: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  return lax.log(sf(x, a, loc, scale))
