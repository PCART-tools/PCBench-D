def _pow_lower(ctx, x, y):
  x_aval, y_aval = ctx.avals_in
  out_aval, = ctx.avals_out
  convert = mlir.lower_fun(
      partial(convert_element_type, new_dtype=out_aval.dtype), False)
  x_aval_ = x_aval.update(dtype=out_aval.dtype)
  y_aval_ = y_aval.update(dtype=out_aval.dtype)
  [(x_,)] = convert(ctx.replace(avals_in=[x_aval], avals_out=[x_aval_]), x)
  [(y_,)] = convert(ctx.replace(avals_in=[y_aval], avals_out=[y_aval_]), y)
  ctx_ = ctx.replace(avals_in=[x_aval_, y_aval_])
  return _nary_lower_hlo(hlo.PowOp, ctx_, x_, y_)
