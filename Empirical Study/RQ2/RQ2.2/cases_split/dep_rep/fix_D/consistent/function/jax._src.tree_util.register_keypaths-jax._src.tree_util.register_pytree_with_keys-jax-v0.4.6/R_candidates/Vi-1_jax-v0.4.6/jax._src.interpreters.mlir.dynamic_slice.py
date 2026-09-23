def dynamic_slice(ctx: LoweringRuleContext, aval_out, x, *,
                  start_indices) -> ir.Value:
  if core.is_opaque_dtype(aval_out.dtype):
    return aval_out.dtype._rules.dynamic_slice_mlir(ctx, aval_out, x,
                                                    start_indices)
  slice_sizes = aval_out.shape
  if not core.is_constant_shape(slice_sizes):
    slice_sizes = eval_dynamic_shape(ctx, slice_sizes)
    return hlo.RealDynamicSliceOp(
        aval_to_ir_type(aval_out), x,
        shape_tensor(start_indices),
        hlo.AddOp(shape_tensor(start_indices),
                  shape_tensor(slice_sizes)).result,
        shape_tensor([1] * len(slice_sizes))
    ).result
  else:
    return hlo.DynamicSliceOp(x, start_indices,
                              dense_int_elements(slice_sizes)).result
