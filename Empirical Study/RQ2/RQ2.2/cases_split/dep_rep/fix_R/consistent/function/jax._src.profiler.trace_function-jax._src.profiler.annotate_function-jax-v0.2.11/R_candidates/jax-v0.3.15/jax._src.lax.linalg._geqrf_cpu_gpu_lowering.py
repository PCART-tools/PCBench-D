def _geqrf_cpu_gpu_lowering(geqrf_impl, batched_geqrf_impl, ctx, a):
  a_aval, taus_aval = ctx.avals_out
  *batch_dims, m, n = a_aval.shape
  batch = prod(batch_dims)

  if batch == 0 or m == 0 or n == 0:
    return mlir.full_like_aval(0, a_aval), mlir.full_like_aval(0, taus_aval)

  if (batched_geqrf_impl is not None and batch > 1 and m // batch <= 128 and
      n // batch <= 128):
    a_out, taus = batched_geqrf_impl(a_aval.dtype, a)
  else:
    a_out, taus, info_geqrf = geqrf_impl(a_aval.dtype, a)
    zeros = mlir.full_like_aval(0, ShapedArray(batch_dims, np.dtype(np.int32)))
    ok = mlir.compare_mhlo(info_geqrf, zeros, "EQ", "SIGNED")
    ok_a = mhlo.BroadcastInDimOp(
          ir.RankedTensorType.get((*batch_dims, 1, 1),
                                  ir.IntegerType.get_signless(1)),
          ok, mlir.dense_int_elements(range(len(batch_dims)))).result
    a_out = _broadcasting_select_mhlo(ok_a, a_out, _nan_like_mhlo(a_aval))
    ok_taus = mhlo.BroadcastInDimOp(
          ir.RankedTensorType.get((*batch_dims, 1,),
                                  ir.IntegerType.get_signless(1)),
          ok, mlir.dense_int_elements(range(len(batch_dims)))).result
    taus = _broadcasting_select_mhlo(ok_taus, taus, _nan_like_mhlo(taus_aval))
  return a_out, taus
