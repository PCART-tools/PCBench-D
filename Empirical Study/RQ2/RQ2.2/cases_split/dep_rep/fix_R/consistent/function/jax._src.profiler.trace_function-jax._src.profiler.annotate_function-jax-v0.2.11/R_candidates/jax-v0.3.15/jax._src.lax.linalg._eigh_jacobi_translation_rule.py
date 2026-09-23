def _eigh_jacobi_translation_rule(ctx, avals_in, avals_out, operand, *, lower,
                                  sort_eigenvalues):
  operand_aval, = avals_in
  if operand_aval.shape[-1] == 0:
    return [xops.Real(xops.Reshape(operand, operand_aval.shape[:-1])), operand]
  v, w = xops.Eigh(operand, lower=lower, sort_eigenvalues=sort_eigenvalues)
  return w, v
