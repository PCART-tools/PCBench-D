def _triangular_solve_gpu_lower(
    trsm_impl, ctx, a, b, *, left_side, lower, transpose_a, conjugate_a,
    unit_diagonal):
  a_aval, _ = ctx.avals_in
  m, n = a_aval.shape[-2:]
  batch = prod(a_aval.shape[:-2])
  if conjugate_a and not transpose_a:
    a = chlo.ConjOp(a).result
    conjugate_a = False
  if batch > 1 and m <= 256 and n <= 256:
    return [trsm_impl(a_aval.dtype, a, b, left_side, lower, transpose_a,
                      conjugate_a, unit_diagonal)]
  else:
    # Use the XLA implementation for unbatched triangular_solve.
    if transpose_a:
      transpose = "ADJOINT" if conjugate_a else "TRANSPOSE"
    else:
      transpose = "NO_TRANSPOSE"
    return mhlo.TriangularSolveOp(b.type, a, b, ir.BoolAttr.get(left_side),
                                  ir.BoolAttr.get(lower),
                                  ir.BoolAttr.get(unit_diagonal),
                                  mhlo.TransposeAttr.get(transpose)).results
