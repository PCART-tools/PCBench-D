def _eig_cpu_lowering(ctx, operand, *, compute_left_eigenvectors,
                      compute_right_eigenvectors):
  operand_aval, = ctx.avals_in
  out_aval = ctx.avals_out[0]
  batch_dims = operand_aval.shape[:-2]

  w, vl, vr, info = lapack.geev_mhlo(operand_aval.dtype, operand,
                                     jobvl=compute_left_eigenvectors,
                                     jobvr=compute_right_eigenvectors)

  ok = mlir.compare_mhlo(
      info, mlir.full_like_aval(0, ShapedArray(batch_dims, np.dtype(np.int32))),
      "EQ", "SIGNED")
  w = _broadcasting_select_mhlo(
      mhlo.BroadcastInDimOp(
          ir.RankedTensorType.get(batch_dims + (1,),
                                  ir.IntegerType.get_signless(1)),
          ok, mlir.dense_int_elements(range(len(batch_dims)))).result,
      w, _nan_like_mhlo(out_aval))
  output = [w]

  if compute_left_eigenvectors:
    aval = ctx.avals_out[len(output)]
    vl = _broadcasting_select_mhlo(
        mhlo.BroadcastInDimOp(
          ir.RankedTensorType.get(batch_dims + (1, 1),
                                  ir.IntegerType.get_signless(1)),
          ok, mlir.dense_int_elements(range(len(batch_dims)))).result,
        vl, _nan_like_mhlo(aval))
    output.append(vl)

  if compute_right_eigenvectors:
    aval = ctx.avals_out[len(output)]
    vr = _broadcasting_select_mhlo(
        mhlo.BroadcastInDimOp(
          ir.RankedTensorType.get(batch_dims + (1, 1),
                                  ir.IntegerType.get_signless(1)),
          ok, mlir.dense_int_elements(range(len(batch_dims)))).result,
        vr, _nan_like_mhlo(aval))
    output.append(vr)

  return output
