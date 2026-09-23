def _cholesky_cpu_gpu_lowering(potrf_impl, ctx, operand):
  operand_aval, = ctx.avals_in
  out_aval, = ctx.avals_out
  batch_dims = operand_aval.shape[:-2]
  result, info = potrf_impl(operand_aval.dtype, operand, lower=True)
  ok = mlir.compare_mhlo(
      info, mlir.full_like_aval(0, ShapedArray(batch_dims, np.dtype(np.int32))),
      "EQ", "SIGNED")
  return [_broadcasting_select_mhlo(
      mhlo.BroadcastInDimOp(
          ir.RankedTensorType.get(batch_dims + (1, 1),
                                  ir.IntegerType.get_signless(1)),
          ok, mlir.dense_int_elements(range(len(batch_dims)))).result,
      result, _nan_like_mhlo(out_aval))]
