def _empty_lower(ctx, *, dtype):
  if core.is_opaque_dtype(dtype):
    return dtype._rules.empty_mlir(ctx, ctx.avals_out[0])
  return mlir.ir_constants(np.zeros((), np.dtype(dtype)))
