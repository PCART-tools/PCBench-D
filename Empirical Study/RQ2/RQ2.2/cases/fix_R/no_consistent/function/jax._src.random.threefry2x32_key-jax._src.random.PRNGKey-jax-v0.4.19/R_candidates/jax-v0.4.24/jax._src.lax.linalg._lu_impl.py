def _lu_impl(operand):
  lu, pivot, perm = dispatch.apply_primitive(lu_p, operand)
  return lu, pivot, perm
