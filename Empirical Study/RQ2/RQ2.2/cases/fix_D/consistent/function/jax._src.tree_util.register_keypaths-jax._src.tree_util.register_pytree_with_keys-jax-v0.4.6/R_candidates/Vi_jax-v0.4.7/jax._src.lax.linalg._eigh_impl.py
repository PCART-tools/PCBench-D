def _eigh_impl(operand, *, lower, sort_eigenvalues):
  v, w = xla.apply_primitive(eigh_p, operand, lower=lower,
                             sort_eigenvalues=sort_eigenvalues)
  return v, w
