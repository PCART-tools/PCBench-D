def _lu_cpu_gpu_lowering(getrf_impl, ctx, operand, *,
                         platform: str):
  operand_aval, = ctx.avals_in
  # It should be possible to support fully-dynamic shapes, but since
  # the last two dimensions (m, n) are used in more involved ways, we only
  # support dynamic dimensions for the batch size for now.
  if not is_constant_shape(operand_aval.shape[-2:]):
    raise NotImplementedError(
      "Shape polymorphism for native lowering for lu on CPU and GPU is "
      f"implemented only for the batch dimensions: {operand_aval.shape}")

  out_aval, pivot_aval, perm_aval = ctx.avals_out
  batch_dims = operand_aval.shape[:-2]
  m = operand_aval.shape[-2]
  if platform in ["cuda", "rocm"]:
    # TODO(necula): remove the platform kwarg when we implement GPU support.
    if not is_constant_shape(operand_aval.shape):
      raise NotImplementedError(
          "Shape polymorphism for native serialization for lu on GPU is not "
          f"implemented; b/261671778; {operand_aval.shape}")
    lu, pivot, info = getrf_impl(operand_aval.dtype, operand)
  else:
    op_shape_vals = mlir.eval_dynamic_shape_as_ivals(ctx, operand_aval.shape)
    lu, pivot, info = getrf_impl(
        operand_aval.dtype, operand, a_shape_vals=op_shape_vals)
  # Subtract 1 from the pivot to get 0-based indices.
  pivot = hlo.subtract(pivot, mlir.full_like_aval(ctx, 1, pivot_aval))
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
