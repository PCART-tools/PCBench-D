def _pow_lowering_rule(ctx: TritonLoweringRuleContext, x: tc.tensor, y: tc.tensor) -> tc.tensor:
  x_aval, y_aval = ctx.avals_in
  y_dtype = y_aval.dtype
  if y_aval.weak_type:
    if jnp.isdtype(y_dtype, "integral"):
      y_dtype = jnp.int32
    else:
      y_dtype = x_aval.dtype
  x = tc.semantic.cast(x, _convert_dtype(x_aval.dtype))
  y = tc.semantic.cast(y, _convert_dtype(y_dtype))
  [out_aval] = ctx.avals_out
  x = tc.broadcast_to(x, out_aval.shape)
  y = tc.broadcast_to(y, out_aval.shape)
  return tc.math.pow(x, y)
