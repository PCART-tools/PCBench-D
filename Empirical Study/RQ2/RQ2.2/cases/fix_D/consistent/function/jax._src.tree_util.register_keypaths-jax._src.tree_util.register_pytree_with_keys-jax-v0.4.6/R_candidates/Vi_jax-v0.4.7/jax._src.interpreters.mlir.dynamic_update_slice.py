def dynamic_update_slice(ctx: LoweringRuleContext, aval_out, x, update, *,
                         start_indices) -> ir.Value:
  if core.is_opaque_dtype(aval_out.dtype):
    return aval_out.dtype._rules.dynamic_update_slice_mlir(
        ctx, aval_out, x, update, *start_indices)

  # TODO(necula): handle dynamic shapes
  return hlo.DynamicUpdateSliceOp(x, update, start_indices).result
