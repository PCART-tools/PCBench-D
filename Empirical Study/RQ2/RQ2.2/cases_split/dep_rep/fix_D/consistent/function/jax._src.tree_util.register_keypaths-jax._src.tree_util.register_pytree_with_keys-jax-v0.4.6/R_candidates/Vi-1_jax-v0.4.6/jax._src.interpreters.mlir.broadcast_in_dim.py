def broadcast_in_dim(ctx: LoweringRuleContext, op, aval_out: core.AbstractValue, *,
                     broadcast_dimensions) -> ir.Value:
  # Lower a possibly-dynamic broadcast_in_dim
  if core.is_opaque_dtype(aval_out.dtype):  # type: ignore
    return aval_out.dtype._rules.broadcast_in_dim_mlir(  # type: ignore
        ctx, aval_out, op,
        broadcast_dimensions=broadcast_dimensions)
  if not core.is_constant_shape(aval_out.shape):  # type: ignore
    shape = eval_dynamic_shape(ctx, aval_out.shape)  # type: ignore
    return hlo.DynamicBroadcastInDimOp(
        aval_to_ir_type(aval_out), op,
        shape_tensor(shape),
        dense_int_elements(broadcast_dimensions),
    ).result
  else:
    return hlo.BroadcastInDimOp(
        aval_to_ir_type(aval_out), op,
        dense_int_elements(broadcast_dimensions)).result
