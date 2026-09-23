@implements(osp_stats.uniform.cdf, update_doc=False)
def cdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, loc, scale = promote_args_inexact("uniform.cdf", x, loc, scale)
  zero, one = jnp.array(0, x.dtype), jnp.array(1, x.dtype)
  conds = [lax.lt(x, loc), lax.gt(x, lax.add(loc, scale)), lax.ge(x, loc) & lax.le(x, lax.add(loc, scale))]
  vals = [zero, one, lax.div(lax.sub(x, loc), scale)]

  return jnp.select(conds, vals)
