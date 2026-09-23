def _threefry2x32_gpu_lowering(lowering_func, ctx, k1, k2, x1, x2):
  aval_out, aval_out_2 = ctx.avals_out
  assert aval_out == aval_out_2
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
    length = mlir.eval_dynamic_shape_as_tensor(ctx, [out_len])
    length = mlir.hlo.convert(
        ir.RankedTensorType.get((1,), ir.IntegerType.get_signless(64)),
        length)
    output_shape = mlir.eval_dynamic_shape_as_tensor(ctx, aval_out.shape)
  else:
    length = int(out_len)  # will be passed statically
    output_shape = None

  return lowering_func(
          (_broadcast(k1, k1_aval), _broadcast(k2, k2_aval)),
          (_broadcast(x1, x1_aval), _broadcast(x2, x2_aval)), length,
          output_shape)
