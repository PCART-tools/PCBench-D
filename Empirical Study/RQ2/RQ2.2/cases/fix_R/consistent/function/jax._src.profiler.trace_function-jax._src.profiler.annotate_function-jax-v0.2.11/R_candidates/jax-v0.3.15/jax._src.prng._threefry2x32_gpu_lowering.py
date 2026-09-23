def _threefry2x32_gpu_lowering(threefry2x32_lowering, ctx, k1, k2, x1, x2):
  aval_out, _ = ctx.avals_out
  k1_aval, k2_aval, x1_aval, x2_aval = ctx.avals_in
  rank = len(aval_out.shape)
  if 0 in aval_out.shape:
    zeros = mlir.full_like_aval(0, aval_out)
    return [zeros, zeros]
  def _broadcast(x, aval):
    return mhlo.BroadcastInDimOp(
        mlir.aval_to_ir_type(aval_out), x,
        mlir.dense_int_elements(range(rank - len(aval.shape), rank))).result
  return threefry2x32_lowering(
          (_broadcast(k1, k1_aval), _broadcast(k2, k2_aval)),
          (_broadcast(x1, x1_aval), _broadcast(x2, x2_aval)))
