@_wraps(osp_stats.t.logpdf, update_doc=False)
def logpdf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, df, loc, scale = promote_args_inexact("t.logpdf", x, df, loc, scale)
  two = _lax_const(x, 2)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  df_over_two = lax.div(df, two)
  df_plus_one_over_two = lax.add(df_over_two, _lax_const(x, 0.5))
  normalize_term_const = lax.mul(lax.mul(scale, scale), _lax_const(x, np.pi))
  normalize_term_tmp = lax.div(lax.log(lax.mul(normalize_term_const, df)), two)
  normalize_term = lax.sub(lax.add(lax.lgamma(df_over_two), normalize_term_tmp),
                           lax.lgamma(df_plus_one_over_two))
  quadratic = lax.div(lax.mul(scaled_x, scaled_x), df)
  return lax.neg(lax.add(normalize_term, lax.mul(df_plus_one_over_two, lax.log1p(quadratic))))
