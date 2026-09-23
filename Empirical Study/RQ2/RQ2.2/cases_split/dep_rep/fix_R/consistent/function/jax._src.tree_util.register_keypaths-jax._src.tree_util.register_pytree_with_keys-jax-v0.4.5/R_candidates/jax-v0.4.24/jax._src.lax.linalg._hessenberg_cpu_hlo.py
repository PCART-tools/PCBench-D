def _hessenberg_cpu_hlo(ctx, a):
  a_aval, = ctx.avals_in
  batch_dims = a_aval.shape[:-2]
  a, taus, info = lapack.gehrd_hlo(a_aval.dtype, a)
  ok = mlir.compare_hlo(
      info, mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.dtype(np.int32))),
      "EQ", "SIGNED")
  select_a_aval = ShapedArray(batch_dims + (1, 1), np.dtype(np.bool_))
  select_taus_aval = ShapedArray(batch_dims + (1,), np.dtype(np.bool_))
  return [
    _broadcasting_select_hlo(
      ctx,
      mlir.broadcast_in_dim(ctx, ok, select_a_aval,
                            broadcast_dimensions=range(len(batch_dims))),
      select_a_aval,
      a, ctx.avals_out[0], _nan_like_hlo(ctx, ctx.avals_out[0]), ctx.avals_out[0]),
    _broadcasting_select_hlo(
      ctx,
      mlir.broadcast_in_dim(ctx, ok, select_taus_aval,
                            broadcast_dimensions=range(len(batch_dims))),
      select_taus_aval,
      taus, ctx.avals_out[1], _nan_like_hlo(ctx, ctx.avals_out[1]), ctx.avals_out[1]),
    ]
