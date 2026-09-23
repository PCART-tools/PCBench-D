@_wraps(osp_stats.beta.logpdf, update_doc=False)
def logpdf(x: ArrayLike, a: ArrayLike, b: ArrayLike,
           loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, a, b, loc, scale = promote_args_inexact("beta.logpdf", x, a, b, loc, scale)
  one = _lax_const(x, 1)
  shape_term = lax.neg(betaln(a, b))
  y = lax.div(lax.sub(x, loc), scale)
  log_linear_term = lax.add(xlogy(lax.sub(a, one), y),
                            xlog1py(lax.sub(b, one), lax.neg(y)))
  log_probs = lax.sub(lax.add(shape_term, log_linear_term), lax.log(scale))
  return jnp.where(jnp.logical_or(lax.gt(x, lax.add(loc, scale)),
                                  lax.lt(x, loc)), -jnp.inf, log_probs)
