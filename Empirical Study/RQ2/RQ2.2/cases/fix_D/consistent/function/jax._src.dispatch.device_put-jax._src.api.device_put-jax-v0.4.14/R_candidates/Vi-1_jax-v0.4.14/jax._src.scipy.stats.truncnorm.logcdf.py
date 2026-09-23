@_wraps(osp_stats.truncnorm.logcdf, update_doc=False)
def logcdf(x, a, b, loc=0, scale=1):
  x, a, b, loc, scale = promote_args_inexact("truncnorm.logcdf", x, a, b, loc, scale)
  x, a, b = jnp.broadcast_arrays(x, a, b)
  x = lax.div(lax.sub(x, loc), scale)
  logcdf = _log_gauss_mass(a, x) - _log_gauss_mass(a, b)
  logsf = _log_gauss_mass(x, b) - _log_gauss_mass(a, b)

  logcdf = jnp.select(
    # third condition: avoid catastrophic cancellation (from scipy)
    [x >= b, x <= a, logcdf > -0.1, x > a],
    [0, -jnp.inf, jnp.log1p(-jnp.exp(logsf)), logcdf]
  )
  logcdf = jnp.where(a >= b, jnp.nan, logcdf)
  return logcdf
