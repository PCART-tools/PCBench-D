@implements(osp_stats.logistic.logpdf, update_doc=False)
def logpdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  x, loc, scale = promote_args_inexact("logistic.logpdf", x, loc, scale)
  x = lax.div(lax.sub(x, loc), scale)
  two = _lax_const(x, 2)
  half_x = lax.div(x, two)
  return lax.sub(lax.mul(lax.neg(two), jnp.logaddexp(half_x, lax.neg(half_x))), lax.log(scale))
