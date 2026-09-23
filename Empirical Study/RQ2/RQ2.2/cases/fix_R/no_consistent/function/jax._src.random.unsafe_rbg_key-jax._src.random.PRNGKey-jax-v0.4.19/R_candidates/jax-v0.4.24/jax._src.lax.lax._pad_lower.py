def _pad_lower(ctx, x, padding_value, *, padding_config):
  aval_out, = ctx.avals_out
  low, high, interior = util.unzip3(padding_config)
  return [mlir.pad(ctx, aval_out, x, padding_value, low, high, interior)]
