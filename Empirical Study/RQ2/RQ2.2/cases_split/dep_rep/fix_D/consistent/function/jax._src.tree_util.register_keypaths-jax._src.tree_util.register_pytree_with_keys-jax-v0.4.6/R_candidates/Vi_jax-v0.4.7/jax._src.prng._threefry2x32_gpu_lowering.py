def _threefry2x32_gpu_lowering(lowering_func, ctx, k1, k2, x1, x2):
  aval_out, _ = ctx.avals_out
  k1_aval, k2_aval, x1_aval, x2_aval = ctx.avals_in
  rank = len(aval_out.shape)
  if 0 in aval_out.shape:
    zeros = mlir.full_like_aval(ctx, 0, aval_out)
    return [zeros, zeros]
  def _broadcast(x, aval):
    return mlir.broadcast_in_dim(ctx, x, aval_out,
                                 broadcast_dimensions=range(rank - len(aval.shape), rank))

  out_len = reduce(op.mul, aval_out.shape, 1)
  if not core.is_constant_dim(out_len):
    length = mlir.shape_tensor(mlir.eval_dynamic_shape(ctx, [out_len]))
    length = mlir.hlo.ConvertOp(
        mlir.ir.RankedTensorType.get((1,), mlir.ir.IntegerType.get_signless(64)),
        length).result
  else:
    length = int(out_len)  # will be passed statically

  return lowering_func(
          (_broadcast(k1, k1_aval), _broadcast(k2, k2_aval)),
          (_broadcast(x1, x1_aval), _broadcast(x2, x2_aval)), length)
