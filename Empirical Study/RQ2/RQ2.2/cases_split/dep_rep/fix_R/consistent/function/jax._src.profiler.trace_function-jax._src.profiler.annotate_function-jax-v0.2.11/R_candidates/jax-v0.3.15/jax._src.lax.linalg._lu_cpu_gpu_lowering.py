def _lu_cpu_gpu_lowering(getrf_impl, ctx, operand):
  operand_aval, = ctx.avals_in
  out_aval, pivot_aval, perm_aval = ctx.avals_out
  batch_dims = operand_aval.shape[:-2]
  m = operand_aval.shape[-2]
  lu, pivot, info = getrf_impl(operand_aval.dtype, operand)
  # Subtract 1 from the pivot to get 0-based indices.
  if jax._src.lib.mlir_api_version < 29:
    op = mhlo.SubOp
  else:
    op = mhlo.SubtractOp
  pivot = op(pivot, mlir.full_like_aval(1, pivot_aval)).result
  ok = mlir.compare_mhlo(
      info, mlir.full_like_aval(0, ShapedArray(batch_dims, np.dtype(np.int32))),
      "GE", "SIGNED")
  lu = _broadcasting_select_mhlo(
      mhlo.BroadcastInDimOp(
          ir.RankedTensorType.get(batch_dims + (1, 1),
                                  ir.IntegerType.get_signless(1)),
          ok, mlir.dense_int_elements(range(len(batch_dims)))).result,
      lu, _nan_like_mhlo(out_aval))
  sub_ctx = ctx.replace(primitive=None, avals_in=[pivot_aval], avals_out=[perm_aval])
  perm_fn = mlir.lower_fun(lambda x: lu_pivots_to_permutation(x, m),
                           multiple_results=False)
  perm, = perm_fn(sub_ctx, pivot)
  return [lu, pivot, perm]
