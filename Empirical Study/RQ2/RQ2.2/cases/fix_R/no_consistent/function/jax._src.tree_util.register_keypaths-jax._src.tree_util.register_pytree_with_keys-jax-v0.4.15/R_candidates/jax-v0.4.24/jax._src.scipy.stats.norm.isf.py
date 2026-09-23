@implements(osp_stats.norm.isf, update_doc=False)
def isf(q: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  return ppf(lax.sub(_lax_const(q, 1), q), loc, scale)
