def reshape(ctx: LoweringRuleContext, op, aval_out: core.AbstractValue) -> ir.Value:
  if core.is_opaque_dtype(aval_out.dtype):  # type: ignore
    # TODO(frostig,mattjj,necula): asserts a single physical aval, and a
    # particular reshape rule (reshape to the output physical aval's shape)
    aval_out, = aval_out.dtype._rules.physical_avals(aval_out)  # type: ignore
  if not core.is_constant_shape(aval_out.shape):  # type: ignore
    shape = eval_dynamic_shape(ctx, aval_out.shape)  # type: ignore
    return hlo.DynamicReshapeOp(
        aval_to_ir_type(aval_out), op,
        shape_tensor(shape),
    ).result
  else:
    return hlo.ReshapeOp(aval_to_ir_type(aval_out), op).result
