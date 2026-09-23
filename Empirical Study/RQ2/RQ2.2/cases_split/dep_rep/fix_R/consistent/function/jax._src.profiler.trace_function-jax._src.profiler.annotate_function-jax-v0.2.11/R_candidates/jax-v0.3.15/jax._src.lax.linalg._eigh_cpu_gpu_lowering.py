def _eigh_cpu_gpu_lowering(syevd_impl, ctx, operand, *, lower,
                           sort_eigenvalues):
  del sort_eigenvalues  # The CPU/GPU implementations always sort.
  operand_aval, = ctx.avals_in
  v_aval, w_aval = ctx.avals_out
  batch_dims = operand_aval.shape[:-2]
  v, w, info = syevd_impl(operand_aval.dtype, operand, lower=lower)
  zeros = mlir.full_like_aval(0, ShapedArray(batch_dims, np.dtype(np.int32)))
  ok = mlir.compare_mhlo(info, zeros, "EQ", "SIGNED")
  v = _broadcasting_select_mhlo(
      mhlo.BroadcastInDimOp(
          ir.RankedTensorType.get(batch_dims + (1, 1),
                                  ir.IntegerType.get_signless(1)),
          ok, mlir.dense_int_elements(range(len(batch_dims)))).result,
      v, _nan_like_mhlo(v_aval))
  w = _broadcasting_select_mhlo(
      mhlo.BroadcastInDimOp(
          ir.RankedTensorType.get(batch_dims + (1,),
                                  ir.IntegerType.get_signless(1)),
          ok, mlir.dense_int_elements(range(len(batch_dims)))).result,
      w, _nan_like_mhlo(w_aval))
  return [v, w]
