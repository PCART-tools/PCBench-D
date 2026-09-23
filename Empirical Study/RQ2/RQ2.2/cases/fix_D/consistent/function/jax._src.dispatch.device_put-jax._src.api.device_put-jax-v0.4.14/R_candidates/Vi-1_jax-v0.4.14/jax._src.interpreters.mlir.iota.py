def iota(ctx: LoweringRuleContext, aval_out, *, dimension: int):
  if not core.is_constant_shape(aval_out.shape):
    shape = eval_dynamic_shape_as_tensor(ctx, aval_out.shape)
    return hlo.DynamicIotaOp(
        aval_to_ir_type(aval_out),
        shape,
        i64_attr(dimension),
    ).result
  else:
    return hlo.IotaOp(aval_to_ir_type(aval_out),
                      i64_attr(dimension)).result
