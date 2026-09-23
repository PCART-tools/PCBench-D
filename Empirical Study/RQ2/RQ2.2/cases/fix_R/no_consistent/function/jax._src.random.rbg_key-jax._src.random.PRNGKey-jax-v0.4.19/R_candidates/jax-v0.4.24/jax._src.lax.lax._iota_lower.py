def _iota_lower(ctx, *dyn_shape, dtype, shape, dimension):
  del dtype
  aval_out, = ctx.avals_out
  if dyn_shape:
    aval_out = aval_out.update(shape=_merge_dyn_shape(shape, dyn_shape))
  return [mlir.iota(ctx, aval_out, dimension=dimension)]
