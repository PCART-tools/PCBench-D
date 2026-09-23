@implements(osp_stats.pareto.logpdf, update_doc=False)
def logpdf(x: ArrayLike, b: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, b, loc, scale = promote_args_inexact("pareto.logpdf", x, b, loc, scale)
  one = _lax_const(x, 1)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  normalize_term = lax.log(lax.div(scale, b))
  log_probs = lax.neg(lax.add(normalize_term, lax.mul(lax.add(b, one), lax.log(scaled_x))))
  return jnp.where(lax.lt(x, lax.add(loc, scale)), -jnp.inf, log_probs)
