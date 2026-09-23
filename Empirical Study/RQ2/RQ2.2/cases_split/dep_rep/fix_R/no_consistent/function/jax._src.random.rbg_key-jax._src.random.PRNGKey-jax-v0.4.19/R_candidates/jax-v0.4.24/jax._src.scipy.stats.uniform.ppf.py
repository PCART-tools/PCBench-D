@implements(osp_stats.uniform.ppf, update_doc=False)
def ppf(q: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  q, loc, scale = promote_args_inexact("uniform.ppf", q, loc, scale)
  return where(
    jnp.isnan(q) | (q < 0) | (q > 1),
    jnp.nan,
    lax.add(loc, lax.mul(scale, q))
  )
