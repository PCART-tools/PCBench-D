def _triangular_solve_cpu_lower(
    ctx, a, b, *, left_side, lower, transpose_a,
    conjugate_a, unit_diagonal):
  a_aval, _ = ctx.avals_in

  if conjugate_a and not transpose_a:
    a = chlo.ConjOp(a).result
    conjugate_a = False
  if len(a_aval.shape) == 2 and np.dtype(a_aval.dtype) in _cpu_lapack_types:
    alpha = mlir.ir_constant(np.array(1, dtype=a_aval.dtype))
    return [lapack.trsm_mhlo(
      a_aval.dtype, alpha,
      a, b, left_side, lower, transpose_a, conjugate_a, unit_diagonal)]
  else:
    # Fall back to the HLO implementation for unsupported types or batching.
    # TODO: Consider swapping XLA for LAPACK in batched case
    if transpose_a:
      transpose = "ADJOINT" if conjugate_a else "TRANSPOSE"
    else:
      transpose = "NO_TRANSPOSE"
    return mhlo.TriangularSolveOp(b.type, a, b, ir.BoolAttr.get(left_side),
                                  ir.BoolAttr.get(lower),
                                  ir.BoolAttr.get(unit_diagonal),
                                  mhlo.TransposeAttr.get(transpose)).results
