@implements(osp_stats.beta.logsf, update_doc=False)
def logsf(x: ArrayLike, a: ArrayLike, b: ArrayLike,
          loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  return lax.log(sf(x, a, b, loc, scale))
