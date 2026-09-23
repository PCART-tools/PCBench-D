def add_jaxvals_lowering(ctx, x, y):
  return hlo.AddOp(x, y).results
