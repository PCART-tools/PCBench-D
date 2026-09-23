@_wraps(osp_stats.chi2.logpdf, update_doc=False)
def logpdf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, df, loc, scale = promote_args_inexact("chi2.logpdf", x, df, loc, scale)
  one = _lax_const(x, 1)
  two = _lax_const(x, 2)
  y = lax.div(lax.sub(x, loc), scale)
  df_on_two = lax.div(df, two)

  kernel = lax.sub(lax.mul(lax.sub(df_on_two, one), lax.log(y)), lax.div(y,two))

  nrml_cnst = lax.neg(lax.add(lax.lgamma(df_on_two),lax.div(lax.mul(lax.log(two), df),two)))

  log_probs = lax.add(lax.sub(nrml_cnst, lax.log(scale)), kernel)
  return jnp.where(lax.lt(x, loc), -jnp.inf, log_probs)
