def _pad_lower(ctx, x, padding_value, *, padding_config):
  low, high, interior = util.unzip3(padding_config)
  return mhlo.PadOp(x, padding_value,
                    mlir.dense_int_elements(low),
                    mlir.dense_int_elements(high),
                    mlir.dense_int_elements(interior)).results
