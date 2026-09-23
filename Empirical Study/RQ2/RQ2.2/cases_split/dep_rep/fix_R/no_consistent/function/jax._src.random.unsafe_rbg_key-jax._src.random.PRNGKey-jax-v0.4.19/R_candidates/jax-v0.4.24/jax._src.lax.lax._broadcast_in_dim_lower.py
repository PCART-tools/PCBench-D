def _broadcast_in_dim_lower(ctx, x, *dyn_shape, shape, broadcast_dimensions) -> Sequence[ir.Value]:
  aval_out, = ctx.avals_out
  if dyn_shape:
    aval_out = aval_out.update(shape=_merge_dyn_shape(shape, dyn_shape))


  return [mlir.broadcast_in_dim(ctx, x, aval_out,
                                broadcast_dimensions=broadcast_dimensions)]
