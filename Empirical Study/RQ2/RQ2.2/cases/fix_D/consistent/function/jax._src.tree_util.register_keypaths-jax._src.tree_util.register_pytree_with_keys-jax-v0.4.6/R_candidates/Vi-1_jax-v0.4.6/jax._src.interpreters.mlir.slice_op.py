def slice_op(ctx: LoweringRuleContext, x, aval_out, *,
             start_indices, limit_indices, strides) -> ir.Value:
  if core.is_opaque_dtype(aval_out.dtype):
    return [aval_out.dtype._rules.slice_mlir(
        ctx, aval_out, x, start_indices, limit_indices, strides)]

  if any(not core.is_constant_shape(s) for s in (start_indices, limit_indices, strides)):
    start_indices = eval_dynamic_shape(ctx, start_indices)
    limit_indices = eval_dynamic_shape(ctx, limit_indices)
    strides = eval_dynamic_shape(ctx, strides)
    return hlo.RealDynamicSliceOp(aval_to_ir_type(aval_out),
                                  x,
                                  shape_tensor(start_indices),
                                  shape_tensor(limit_indices),
                                  shape_tensor(strides)).result
  else:
    return hlo.SliceOp(x,
                       dense_int_elements(start_indices),
                       dense_int_elements(limit_indices),
                       dense_int_elements(strides)).result
