def _schur_cpu_lowering(ctx, operand, *, compute_schur_vectors, sort_eig_vals,
                        select_callable):
  operand_aval, = ctx.avals_in
  batch_dims = operand_aval.shape[:-2]

  gees_result = lapack.gees_mhlo(operand_aval.dtype, operand,
                                  jobvs=compute_schur_vectors,
                                  sort=sort_eig_vals,
                                  select=select_callable)
  # Number of return values depends on value of sort_eig_vals.
  T, vs, *_, info = gees_result

  ok = mlir.compare_mhlo(
      info, mlir.full_like_aval(0, ShapedArray(batch_dims, np.dtype(np.int32))),
      "EQ", "SIGNED")

  T = _broadcasting_select_mhlo(
      mhlo.BroadcastInDimOp(
          ir.RankedTensorType.get(batch_dims + (1, 1),
                                  ir.IntegerType.get_signless(1)),
          ok,
          mlir.dense_int_elements(range(len(batch_dims)))).result,
      T, _nan_like_mhlo(ctx.avals_out[0]))
  output = [T]
  if compute_schur_vectors:
    vs = _broadcasting_select_mhlo(
        mhlo.BroadcastInDimOp(
            ir.RankedTensorType.get(batch_dims + (1, 1),
                                    ir.IntegerType.get_signless(1)),
            ok,
            mlir.dense_int_elements(range(len(batch_dims)))).result,
        vs, _nan_like_mhlo(ctx.avals_out[1]))

    output.append(vs)

  return output
