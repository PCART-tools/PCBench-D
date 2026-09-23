def _lu_impl(operand):
  lu, pivot, perm = xla.apply_primitive(lu_p, operand)
  return lu, pivot, perm
