def pad(ctx: LoweringRuleContext, aval_out,
        x, padding_value,
        padding_low, padding_high, padding_interior) -> ir.Value:
  if all(core.is_constant_shape(s) for s in (padding_low,
                                             padding_high, padding_interior)):
    return hlo.pad(x, padding_value,
                   dense_int_array(padding_low),
                   dense_int_array(padding_high),
                   dense_int_array(padding_interior))
  else:
    padding_low = eval_dynamic_shape_as_tensor(ctx, padding_low)
    padding_high = eval_dynamic_shape_as_tensor(ctx, padding_high)
    padding_interior = eval_dynamic_shape_as_tensor(ctx, padding_interior)
    return hlo.dynamic_pad(
        aval_to_ir_type(aval_out),
        x, padding_value, padding_low, padding_high, padding_interior)
