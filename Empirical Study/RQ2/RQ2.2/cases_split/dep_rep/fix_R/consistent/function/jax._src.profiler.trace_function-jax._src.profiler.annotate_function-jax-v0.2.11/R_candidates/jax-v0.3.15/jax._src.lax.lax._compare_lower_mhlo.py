def _compare_lower_mhlo(direction: str, ctx, x, y):
  x_aval, y_aval = ctx.avals_in
  aval_out, = ctx.avals_out
  x, y = broadcast_mhlo(aval_out.update(dtype=x_aval.dtype), ctx.avals_in,
                        (x, y))
  if dtypes.issubdtype(x_aval.dtype, np.inexact):
    compare_type = "FLOAT"
  elif dtypes.issubdtype(x_aval.dtype, np.signedinteger):
    compare_type = "SIGNED"
  else:
    compare_type = "UNSIGNED"
  return mlir.compare_mhlo(x, y, direction, compare_type).results
