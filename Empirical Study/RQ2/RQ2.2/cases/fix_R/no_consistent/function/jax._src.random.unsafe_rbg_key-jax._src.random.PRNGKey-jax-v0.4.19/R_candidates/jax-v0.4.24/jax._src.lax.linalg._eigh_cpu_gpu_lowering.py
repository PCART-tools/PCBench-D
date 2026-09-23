def _eigh_cpu_gpu_lowering(
    syevd_impl, ctx, operand, *, lower, sort_eigenvalues, subset_by_index
):
  del sort_eigenvalues  # The CPU/GPU implementations always sort.
  operand_aval, = ctx.avals_in
  v_aval, w_aval = ctx.avals_out
  n = operand_aval.shape[-1]
  batch_dims = operand_aval.shape[:-2]

  # The eigh implementation on CPU and GPU uses lapack helper routines to
  # find the size of the workspace based on the non-batch dimensions.
  # Therefore, we cannot yet support dynamic non-batch dimensions.
  if not is_constant_shape(operand_aval.shape[-2:]):
    raise NotImplementedError(
        "Shape polymorphism for native lowering for eigh is implemented "
        f"only for the batch dimensions: {operand_aval.shape}")

  if not (subset_by_index is None or subset_by_index == (0, n)):
    raise NotImplementedError("subset_by_index not implemented for CPU and GPU")

  op_shape_vals = mlir.eval_dynamic_shape_as_ivals(ctx, operand_aval.shape)
  v, w, info = syevd_impl(operand_aval.dtype, operand,
                          a_shape_vals=op_shape_vals, lower=lower)

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
