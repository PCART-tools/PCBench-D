@_wraps(osp_stats.logistic.sf, update_doc=False)
def sf(x):
  return expit(lax.neg(x))
