@implements(osp_stats.gamma.cdf, update_doc=False)
def cdf(x: ArrayLike, a: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, a, loc, scale = promote_args_inexact("gamma.cdf", x, a, loc, scale)
  return gammainc(
    a,
    lax.clamp(
      _lax_const(x, 0),
      lax.div(lax.sub(x, loc), scale),
      _lax_const(x, jnp.inf),
    )
  )
