def _householder_product_cpu_gpu_lowering(orgqr_impl, ctx, a, taus, *,
                                          platform: str):
  a_aval, taus_aval = ctx.avals_in
  *batch_dims, m, n = a_aval.shape
  if not is_constant_shape([m, n]):
    raise NotImplementedError(
      "Shape polymorphism for native serialization for householder_product on "
      f"CPU and GPU is implemented only for the batch dimensions: {a_aval.shape}")

  if m == 0 or n == 0:
    return [mlir.full_like_aval(ctx, 0, a_aval)]

  if platform in ["rocm", "cuda"]:
    # TODO(necula): remove the platform kwarg when we implement GPU support.
    if not is_constant_shape(a_aval.shape):
      raise NotImplementedError(
          "Shape polymorphism for native serialization for householder_product "
          f"on GPU is not implemented; b/261671778; {a_aval.shape}")
    a, info_orgqr = orgqr_impl(a_aval.dtype, a, taus)  # type: ignore
  else:
    a_shape_vals = mlir.eval_dynamic_shape_as_ivals(ctx, a_aval.shape)
    tau_shape_vals = mlir.eval_dynamic_shape_as_ivals(ctx, taus_aval.shape)
    a, info_orgqr = orgqr_impl(a_aval.dtype, a, taus,
                               a_shape_vals=a_shape_vals,
                               tau_shape_vals=tau_shape_vals)
  zeros = mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.dtype(np.int32)))
  ok = mlir.compare_hlo(info_orgqr, zeros, "EQ", "SIGNED")
  select_a_aval = ShapedArray(batch_dims + [1, 1], np.dtype(np.bool_))
  ok = mlir.broadcast_in_dim(ctx, ok, select_a_aval,
                             broadcast_dimensions=range(len(batch_dims)))
  a = _broadcasting_select_hlo(ctx, ok, select_a_aval, a, a_aval, _nan_like_hlo(ctx, a_aval), a_aval)
  return [a]
