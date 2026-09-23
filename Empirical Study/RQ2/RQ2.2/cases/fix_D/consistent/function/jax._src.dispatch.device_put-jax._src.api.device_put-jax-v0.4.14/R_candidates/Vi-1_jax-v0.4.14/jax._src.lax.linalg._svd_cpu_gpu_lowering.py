def _svd_cpu_gpu_lowering(gesvd_impl, ctx, operand, *, full_matrices,
                          compute_uv, platform: str):
  operand_aval, = ctx.avals_in
  s_aval = ctx.avals_out[0]
  m, n = operand_aval.shape[-2:]
  # Since the last two dimensions (m, n) are used to compute the workspace
  # size, we support dynamic dimensions only for the batch size for now.
  if not is_constant_shape([m, n]):
    raise NotImplementedError(
      "Shape polymorphism for native serialization for svd on CPU and GPU is "
      f"implemented only for the batch dimensions: {operand_aval.shape}")
  batch_dims = operand_aval.shape[:-2]

  if m == 0 or n == 0:
    return mlir.lower_fun(_empty_svd, multiple_results=True)(
      ctx, operand, full_matrices=full_matrices, compute_uv=compute_uv)

  if platform in ["cuda", "rocm"] or jaxlib_version < (0, 4, 13):
    if not is_constant_shape(operand_aval.shape):
      # TODO(necula): remove the platform kwarg when we implement GPU support.
      raise NotImplementedError(
          "Shape polymorphism for native serialization for SVD is not "
          f"implemented, try to upgrade jaxlib; b/261671778; {operand_aval.shape}")
    s, u, vt, info = gesvd_impl(operand_aval.dtype, operand,
                                full_matrices=full_matrices,
                                compute_uv=compute_uv)
  else:
    a_shape_vals = mlir.eval_dynamic_shape_as_ivals(ctx, operand_aval.shape)
    s, u, vt, info = gesvd_impl(operand_aval.dtype, operand,
                                full_matrices=full_matrices,
                                compute_uv=compute_uv,
                                a_shape_vals=a_shape_vals)
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
