  def rule(ctx: TritonLoweringRuleContext, x, y, fn=fn, p=prim):
    x_aval, y_aval = ctx.avals_in
    # TODO(slebedev): This is only here for constants. Find a better way.
    x = tc.semantic.cast(x, _convert_dtype(x_aval.dtype))
    y = tc.semantic.cast(y, _convert_dtype(y_aval.dtype))
    [out_aval] = ctx.avals_out
    x = tc.broadcast_to(x, out_aval.shape)
    y = tc.broadcast_to(y, out_aval.shape)
    return fn(x, y)
