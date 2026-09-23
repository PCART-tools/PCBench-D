def _lu_cpu_gpu_lowering(getrf_impl, ctx, operand):
  if any(not is_constant_shape(a.shape) for a in (ctx.avals_in + ctx.avals_out)):
    raise NotImplementedError("Shape polymorphism for custom call is not implemented (lu); b/261671778")
  operand_aval, = ctx.avals_in
  out_aval, pivot_aval, perm_aval = ctx.avals_out
  batch_dims = operand_aval.shape[:-2]
  m = operand_aval.shape[-2]
  lu, pivot, info = getrf_impl(operand_aval.dtype, operand)
  # Subtract 1 from the pivot to get 0-based indices.
  pivot = hlo.SubtractOp(pivot, mlir.full_like_aval(ctx, 1, pivot_aval)).result
  ok = mlir.compare_hlo(
      info, mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.dtype(np.int32))),
      "GE", "SIGNED")
  select_lu_aval = ShapedArray(batch_dims + (1, 1), np.dtype(np.bool_))
  lu = _broadcasting_select_hlo(
      ctx,
      mlir.broadcast_in_dim(ctx, ok, select_lu_aval,
                            broadcast_dimensions=range(len(batch_dims))),
      select_lu_aval,
      lu, out_aval, _nan_like_hlo(ctx, out_aval), out_aval)
  sub_ctx = ctx.replace(primitive=None, avals_in=[pivot_aval], avals_out=[perm_aval])
  perm_fn = mlir.lower_fun(lambda x: lu_pivots_to_permutation(x, m),
                           multiple_results=False)
  perm, = perm_fn(sub_ctx, pivot)
  return [lu, pivot, perm]
