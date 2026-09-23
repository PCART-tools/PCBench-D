def _householder_product_cpu_gpu_lowering(orgqr_impl, ctx, a, taus):
  if any(not is_constant_shape(a.shape) for a in (ctx.avals_in + ctx.avals_out)):
    raise NotImplementedError("Shape polymorphism for custom call is not implemented (householder product); b/261671778")
  a_aval, _ = ctx.avals_in
  *batch_dims, m, n = a_aval.shape

  if m == 0 or n == 0:
    return [mlir.full_like_aval(ctx, 0, a_aval)]

  a, info_orgqr = orgqr_impl(a_aval.dtype, a, taus)
  zeros = mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.dtype(np.int32)))
  ok = mlir.compare_hlo(info_orgqr, zeros, "EQ", "SIGNED")
  select_a_aval = ShapedArray(batch_dims + [1, 1], np.dtype(np.bool_))
  ok = mlir.broadcast_in_dim(ctx, ok, select_a_aval,
                             broadcast_dimensions=range(len(batch_dims)))
  a = _broadcasting_select_hlo(ctx, ok, select_a_aval, a, a_aval, _nan_like_hlo(ctx, a_aval), a_aval)
  return [a]
