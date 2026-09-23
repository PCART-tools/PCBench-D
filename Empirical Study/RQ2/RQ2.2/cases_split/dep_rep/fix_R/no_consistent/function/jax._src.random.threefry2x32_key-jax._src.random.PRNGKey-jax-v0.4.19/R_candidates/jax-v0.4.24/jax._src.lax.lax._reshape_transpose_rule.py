def _reshape_transpose_rule(t, operand, *, new_sizes, dimensions):
  assert ad.is_undefined_primal(operand)
  if dimensions is None:
    return [reshape(t, operand.aval.shape)]
  else:
    return [transpose(reshape(t, np.take(operand.aval.shape, dimensions)),
                      np.argsort(dimensions))]
