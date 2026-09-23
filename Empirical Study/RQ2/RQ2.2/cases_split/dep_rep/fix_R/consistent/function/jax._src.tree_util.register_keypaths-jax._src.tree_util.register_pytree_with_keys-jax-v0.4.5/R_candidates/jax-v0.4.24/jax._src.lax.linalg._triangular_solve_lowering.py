def _triangular_solve_lowering(
    ctx, a, b, *, left_side, lower, transpose_a, conjugate_a, unit_diagonal):
  out_aval, = ctx.avals_out
  if conjugate_a and not transpose_a:
    a = chlo.ConjOp(a)
    conjugate_a = False
  if not transpose_a:
    transpose = "NO_TRANSPOSE"
  else:
    transpose = "ADJOINT" if conjugate_a else "TRANSPOSE"
  return [hlo.triangular_solve(
      a, b, ir.BoolAttr.get(left_side),
      ir.BoolAttr.get(lower), ir.BoolAttr.get(unit_diagonal),
      hlo.TransposeAttr.get(transpose))]
