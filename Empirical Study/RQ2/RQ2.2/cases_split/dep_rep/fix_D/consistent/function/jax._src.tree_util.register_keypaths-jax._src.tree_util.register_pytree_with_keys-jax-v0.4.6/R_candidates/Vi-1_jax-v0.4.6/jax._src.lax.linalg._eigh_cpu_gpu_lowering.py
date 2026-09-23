def _eigh_cpu_gpu_lowering(syevd_impl, ctx, operand, *, lower,
                           sort_eigenvalues):
  if any(not is_constant_shape(a.shape) for a in (ctx.avals_in + ctx.avals_out)):
    raise NotImplementedError("Shape polymorphism for custom call is not implemented (eigh); b/261671778")

  del sort_eigenvalues  # The CPU/GPU implementations always sort.
  operand_aval, = ctx.avals_in
  v_aval, w_aval = ctx.avals_out
  batch_dims = operand_aval.shape[:-2]
  v, w, info = syevd_impl(operand_aval.dtype, operand, lower=lower)
  zeros = mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.dtype(np.int32)))
  ok = mlir.compare_hlo(info, zeros, "EQ", "SIGNED")
  select_v_aval = ShapedArray(batch_dims + (1, 1), np.dtype(np.bool_))
  v = _broadcasting_select_hlo(
      ctx,
      mlir.broadcast_in_dim(ctx, ok, select_v_aval,
                            broadcast_dimensions=range(len(batch_dims))),
      select_v_aval,
      v, v_aval, _nan_like_hlo(ctx, v_aval), v_aval)
  select_w_aval = ShapedArray(batch_dims + (1,), np.dtype(np.bool_))
  w = _broadcasting_select_hlo(
      ctx,
      mlir.broadcast_in_dim(ctx, ok, select_w_aval,
                            broadcast_dimensions=range(len(batch_dims))),
      select_w_aval,
      w, w_aval, _nan_like_hlo(ctx, w_aval), w_aval)
  return [v, w]
