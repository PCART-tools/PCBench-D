def _cholesky_cpu_gpu_lowering(potrf_impl, ctx, operand):
  if any(not is_constant_shape(a.shape) for a in (ctx.avals_in + ctx.avals_out)):
    raise NotImplementedError("Shape polymorphism for custom call is not implemented (cholesky); b/261671778")
  operand_aval, = ctx.avals_in
  out_aval, = ctx.avals_out
  batch_dims = operand_aval.shape[:-2]
  result, info = potrf_impl(operand_aval.dtype, operand, lower=True)
  ok = mlir.compare_hlo(
      info, mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.dtype(np.int32))),
      "EQ", "SIGNED")
  select_aval = ShapedArray(batch_dims + (1, 1), np.dtype(np.bool_))
  return [_broadcasting_select_hlo(
      ctx,
      mlir.broadcast_in_dim(ctx, ok,
                            select_aval,
                            broadcast_dimensions=range(len(batch_dims))),
      select_aval,
      result, out_aval, _nan_like_hlo(ctx, out_aval), out_aval)]
