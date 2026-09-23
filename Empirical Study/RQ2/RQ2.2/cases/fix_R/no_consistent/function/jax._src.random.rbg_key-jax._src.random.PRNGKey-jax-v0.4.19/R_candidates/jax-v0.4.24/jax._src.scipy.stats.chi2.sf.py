@implements(osp_stats.chi2.sf, update_doc=False)
def sf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, df, loc, scale = promote_args_inexact("chi2.sf", x, df, loc, scale)
  two = _lax_const(scale, 2)
  return gammaincc(
    lax.div(df, two),
    lax.clamp(
      _lax_const(x, 0),
      lax.div(
        lax.sub(x, loc),
        lax.mul(scale, two),
      ),
      _lax_const(x, jnp.inf),
    ),
  )
