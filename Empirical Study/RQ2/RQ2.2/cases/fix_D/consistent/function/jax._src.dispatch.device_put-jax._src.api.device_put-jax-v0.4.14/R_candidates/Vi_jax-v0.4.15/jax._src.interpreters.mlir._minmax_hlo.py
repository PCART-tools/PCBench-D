def _minmax_hlo(op, cmp, x, y):
  """Min/max that compares complex values lexicographically as pairs."""
  tensor_type = ir.RankedTensorType(x.type)
  if ir.ComplexType.isinstance(tensor_type.element_type):
    rx = hlo.RealOp(x).result
    ry = hlo.RealOp(y).result
    real_eq = compare_hlo(rx, ry, "EQ", "FLOAT")
    real_cmp = compare_hlo(rx, ry, cmp, "FLOAT")
    imag_cmp = compare_hlo(
        hlo.ImagOp(x).result,
        hlo.ImagOp(y).result, cmp, "FLOAT")
    which = hlo.SelectOp(real_eq, imag_cmp, real_cmp).result
    return hlo.SelectOp(which, x, y)
  else:
    return op(x, y)
