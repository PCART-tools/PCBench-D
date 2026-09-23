@implements(osp_stats.truncnorm.logsf, update_doc=False)
def logsf(x, a, b, loc=0, scale=1):
  x, a, b, loc, scale = promote_args_inexact("truncnorm.logsf", x, a, b, loc, scale)
  return logcdf(-x, -b, -a, -loc, scale)
