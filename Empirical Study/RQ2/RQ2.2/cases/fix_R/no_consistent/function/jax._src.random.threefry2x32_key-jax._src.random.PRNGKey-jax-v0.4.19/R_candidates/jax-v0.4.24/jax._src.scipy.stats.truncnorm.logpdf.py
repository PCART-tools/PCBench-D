@implements(osp_stats.truncnorm.logpdf, update_doc=False)
def logpdf(x, a, b, loc=0, scale=1):
  x, a, b, loc, scale = promote_args_inexact("truncnorm.logpdf", x, a, b, loc, scale)
  val = lax.sub(norm.logpdf(x, loc, scale), _log_gauss_mass(a, b))

  x_scaled = lax.div(lax.sub(x, loc), scale)
  val = jnp.where((x_scaled < a) | (x_scaled > b), -jnp.inf, val)
  val = jnp.where(a >= b, jnp.nan, val)
  return val
