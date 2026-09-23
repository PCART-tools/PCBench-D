def add_jaxvals_lowering(ctx, x, y):
  if (isinstance(a := ctx.avals_in[0], core.ShapedArray) and
      dtypes.issubdtype(a.dtype, dtypes.extended)):
    return lower_fun(lambda x, y: [a.dtype._rules.add(a.dtype, x, y)])(ctx, x, y)  # type: ignore
  return [hlo.add(x, y)]
