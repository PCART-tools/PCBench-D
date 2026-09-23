@implements(osp_stats.norm.ppf, update_doc=False)
def ppf(q: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  return jnp.asarray(special.ndtri(q) * scale + loc, float)
