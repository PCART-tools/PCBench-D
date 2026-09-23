def _svd_cpu_gpu_lowering(gesvd_impl, ctx, operand, *, full_matrices,
                          compute_uv):
  if any(not is_constant_shape(a.shape) for a in (ctx.avals_in + ctx.avals_out)):
    raise NotImplementedError("Shape polymorphism for custom call is not implemented (svd); b/261671778")
  operand_aval, = ctx.avals_in
  s_aval = ctx.avals_out[0]
  m, n = operand_aval.shape[-2:]
  batch_dims = operand_aval.shape[:-2]

  if m == 0 or n == 0:
    return mlir.lower_fun(_empty_svd, multiple_results=True)(
      ctx, operand, full_matrices=full_matrices, compute_uv=compute_uv)

  s, u, vt, info = gesvd_impl(operand_aval.dtype, operand,
                              full_matrices=full_matrices,
                              compute_uv=compute_uv)
  zeros = mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.dtype(np.int32)))
  ok = mlir.compare_hlo(info, zeros, "EQ", "SIGNED")
  select_s_aval = ShapedArray(batch_dims + (1,), np.dtype(np.bool_))
  s = _broadcasting_select_hlo(
      ctx,
      mlir.broadcast_in_dim(ctx, ok, select_s_aval,
                            broadcast_dimensions=range(len(batch_dims))),
      select_s_aval,
      s, s_aval, _nan_like_hlo(ctx, s_aval), s_aval)
  result = [s]

  if compute_uv:
    u_aval, vt_aval = ctx.avals_out[1:]
    select_u_aval = ShapedArray(batch_dims + (1, 1), np.dtype(np.bool_))
    u = _broadcasting_select_hlo(
        ctx,
        mlir.broadcast_in_dim(ctx, ok, select_u_aval,
                              broadcast_dimensions=range(len(batch_dims))),
        select_u_aval,
        u, u_aval, _nan_like_hlo(ctx, u_aval), u_aval)
    select_v_aval = ShapedArray(batch_dims + (1, 1), np.dtype(np.bool_))
    vt = _broadcasting_select_hlo(
        ctx,
        mlir.broadcast_in_dim(ctx, ok, select_v_aval,
                              broadcast_dimensions=range(len(batch_dims))),
        select_v_aval,
        vt, vt_aval, _nan_like_hlo(ctx, vt_aval), vt_aval)
    result += [u, vt]

  return result
