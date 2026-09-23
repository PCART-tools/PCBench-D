def _orgqr_cpu_gpu_lowering(orgqr_impl, ctx, a, taus):
  a_aval, _ = ctx.avals_in
  *batch_dims, m, n = a_aval.shape

  if m == 0 or n == 0:
    return [mlir.full_like_aval(0, a_aval)]

  a, info_orgqr = orgqr_impl(a_aval.dtype, a, taus)
  zeros = mlir.full_like_aval(0, ShapedArray(batch_dims, np.dtype(np.int32)))
  ok = mlir.compare_mhlo(info_orgqr, zeros, "EQ", "SIGNED")
  ok = mhlo.BroadcastInDimOp(
        ir.RankedTensorType.get((*batch_dims, 1, 1),
                                ir.IntegerType.get_signless(1)),
        ok, mlir.dense_int_elements(range(len(batch_dims)))).result
  a = _broadcasting_select_mhlo(ok, a, _nan_like_mhlo(a_aval))
  return [a]
