def _cholesky_cpu_lowering(ctx, operand):
  operand_aval, = ctx.avals_in
  out_aval, = ctx.avals_out
  batch_dims = operand_aval.shape[:-2]
  if jaxlib_version < (0, 4, 13):
    if not is_constant_shape(operand_aval.shape):
      raise NotImplementedError(
          "Shape polymorphism for native serialization for cholesky on CPU is "
          f"not implemented; b/261671778; {operand_aval.shape}")
    result, info = lapack.potrf_hlo(operand_aval.dtype, operand, lower=True)  # type: ignore
  else:
    op_shape_vals = mlir.eval_dynamic_shape_as_ivals(ctx, operand_aval.shape)
    result, info = lapack.potrf_hlo(operand_aval.dtype, operand, lower=True,
                                    a_shape_vals=op_shape_vals)

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
