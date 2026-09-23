def _mul_transpose(ct, x, y):
  assert ad.is_undefined_primal(x) ^ ad.is_undefined_primal(y)
  if ad.is_undefined_primal(x):
    if type(ct) is ad_util.Zero:
      return [ad_util.Zero(x.aval), None]
    else:
      return [_unbroadcast(x.aval, mul(ct, y)), None]
  else:
    if type(ct) is ad_util.Zero:
      return [None, ad_util.Zero(y.aval)]
    else:
      return [None, _unbroadcast(y.aval, mul(x, ct))]
