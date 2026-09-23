def precision_attr(precision: PrecisionType) -> ir.ArrayAttr:
  if precision is None:
    full_precision = (Precision.DEFAULT, Precision.DEFAULT)
  elif not isinstance(precision, tuple):
    full_precision = (precision, precision)
  else:
    full_precision = precision
  return ir.ArrayAttr.get(
      [mhlo.PrecisionAttr.get(str(p)) for p in full_precision])
