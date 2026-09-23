def _select_n_lowering_rule(ctx: LoweringRuleContext, pred, x, *args):
  if len(args) > 1:
    raise NotImplementedError("select_n only supported with <= 2 arguments")
  pred_aval, x_aval = ctx.avals_in[:2]
  pred = _canonicalize_value(pred, dtype=pred_aval.dtype)
  if pred_aval.dtype != np.dtype(np.bool_):
    lower_ctx = LoweringRuleContext(
        ctx.lowering_context,
        avals_in=[pred_aval],
        avals_out=[pred_aval.update(dtype=np.bool_)],
        block_shapes=[None],
    )
    pred = lower_fun(lambda x: x != 0, multiple_results=False)(lower_ctx, pred)
  x_dtype = x_aval.dtype
  x = _canonicalize_value(x, dtype=x_dtype)
  if not args:
    return x
  args = map(partial(_canonicalize_value, dtype=x_dtype), args)
  # Assume x and y
  y, = args
  return arith.SelectOp(pred, y, x).result
