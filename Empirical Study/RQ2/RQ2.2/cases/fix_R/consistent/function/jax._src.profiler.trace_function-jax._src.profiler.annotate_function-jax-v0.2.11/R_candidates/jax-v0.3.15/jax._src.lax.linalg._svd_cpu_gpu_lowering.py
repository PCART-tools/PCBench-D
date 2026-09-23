def _svd_cpu_gpu_lowering(gesvd_impl, ctx, operand, *, full_matrices,
                          compute_uv):
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
  zeros = mlir.full_like_aval(0, ShapedArray(batch_dims, np.dtype(np.int32)))
  ok = mlir.compare_mhlo(info, zeros, "EQ", "SIGNED")
  s = _broadcasting_select_mhlo(
      mhlo.BroadcastInDimOp(
          ir.RankedTensorType.get(batch_dims + (1,),
                                  ir.IntegerType.get_signless(1)),
          ok, mlir.dense_int_elements(range(len(batch_dims)))).result,
      s, _nan_like_mhlo(s_aval))
  result = [s]

  if compute_uv:
    u_aval, vt_aval = ctx.avals_out[1:]
    u = _broadcasting_select_mhlo(
        mhlo.BroadcastInDimOp(
            ir.RankedTensorType.get(batch_dims + (1, 1),
                                    ir.IntegerType.get_signless(1)),
            ok, mlir.dense_int_elements(range(len(batch_dims)))).result,
        u, _nan_like_mhlo(u_aval))
    vt = _broadcasting_select_mhlo(
        mhlo.BroadcastInDimOp(
            ir.RankedTensorType.get(batch_dims + (1, 1),
                                    ir.IntegerType.get_signless(1)),
            ok, mlir.dense_int_elements(range(len(batch_dims)))).result,
        vt, _nan_like_mhlo(vt_aval))
    result += [u, vt]

  return result
