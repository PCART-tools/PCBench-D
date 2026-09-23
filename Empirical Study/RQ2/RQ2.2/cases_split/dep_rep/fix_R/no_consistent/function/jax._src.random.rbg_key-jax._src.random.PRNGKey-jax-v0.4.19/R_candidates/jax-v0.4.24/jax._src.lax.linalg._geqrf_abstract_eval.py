def _geqrf_abstract_eval(operand):
  if not isinstance(operand, ShapedArray):
    raise NotImplementedError("Unsupported aval in geqrf_abstract_eval: "
                              f"{operand.aval}")
  if operand.ndim < 2:
    raise ValueError("Argument to QR decomposition must have ndims >= 2")
  *batch_dims, m, n = operand.shape
  taus = operand.update(shape=(*batch_dims, min(m, n)))
  return operand, taus
