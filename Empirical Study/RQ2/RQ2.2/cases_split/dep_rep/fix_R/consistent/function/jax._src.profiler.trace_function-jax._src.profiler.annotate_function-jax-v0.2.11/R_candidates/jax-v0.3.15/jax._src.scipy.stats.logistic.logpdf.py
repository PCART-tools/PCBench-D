@_wraps(osp_stats.logistic.logpdf, update_doc=False)
def logpdf(x):
  x, = _promote_args_inexact("logistic.logpdf", x)
  two = _lax_const(x, 2)
  half_x = lax.div(x, two)
  return lax.mul(lax.neg(two), jnp.logaddexp(half_x, lax.neg(half_x)))
