def iota(ctx: LoweringRuleContext, aval_out, *, dimension: int):
  if not core.is_constant_shape(aval_out.shape):
    shape = eval_dynamic_shape_as_tensor(ctx, aval_out.shape)
    return hlo.dynamic_iota(
        aval_to_ir_type(aval_out),
        shape,
        i64_attr(dimension),
    )
  else:
    return hlo.iota(aval_to_ir_type(aval_out), i64_attr(dimension))
