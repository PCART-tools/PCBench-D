def _eigh_jacobi_impl(operand, *, lower, sort_eigenvalues):
  w, v = dispatch.apply_primitive(eigh_jacobi_p, operand, lower=lower,
                                  sort_eigenvalues=sort_eigenvalues)
  return w, v
