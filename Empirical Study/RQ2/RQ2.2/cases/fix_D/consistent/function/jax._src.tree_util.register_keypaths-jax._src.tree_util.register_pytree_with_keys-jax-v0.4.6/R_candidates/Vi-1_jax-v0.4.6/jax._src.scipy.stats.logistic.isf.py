@_wraps(osp_stats.logistic.isf, update_doc=False)
def isf(x):
  return -logit(x)
