def _triangular_solve_cpu_lower(
    ctx, a, b, *, left_side, lower, transpose_a,
    conjugate_a, unit_diagonal):
  a_aval, b_aval = ctx.avals_in

  if conjugate_a and not transpose_a:
    a = chlo.conj(a)
    conjugate_a = False
  if len(a_aval.shape) == 2 and np.dtype(a_aval.dtype) in _cpu_lapack_types:
    alpha = mlir.ir_constant(np.array(1, dtype=a_aval.dtype))
    b_shape_vals = mlir.eval_dynamic_shape_as_ivals(ctx, b_aval.shape)
    return [lapack.trsm_hlo(
      a_aval.dtype, alpha,
      a, b, left_side, lower, transpose_a, conjugate_a, unit_diagonal,
      b_shape_vals=b_shape_vals)]
  else:
    # Fall back to the HLO implementation for unsupported types or batching.
    # TODO: Consider swapping XLA for LAPACK in batched case
    if transpose_a:
      transpose = "ADJOINT" if conjugate_a else "TRANSPOSE"
    else:
      transpose = "NO_TRANSPOSE"
    return [hlo.triangular_solve(a, b, ir.BoolAttr.get(left_side),
                                 ir.BoolAttr.get(lower),
                                 ir.BoolAttr.get(unit_diagonal),
                                 hlo.TransposeAttr.get(transpose))]
