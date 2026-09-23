def reshape(ctx: LoweringRuleContext, op, aval_out: core.AbstractValue) -> ir.Value:
  aval_out = core.physical_aval(aval_out)
  if not core.is_constant_shape(aval_out.shape):  # type: ignore
    shape = eval_dynamic_shape_as_tensor(ctx, aval_out.shape)  # type: ignore
    return hlo.DynamicReshapeOp(
        aval_to_ir_type(aval_out), op, shape,
    ).result
  else:
    return hlo.ReshapeOp(aval_to_ir_type(aval_out), op).result
