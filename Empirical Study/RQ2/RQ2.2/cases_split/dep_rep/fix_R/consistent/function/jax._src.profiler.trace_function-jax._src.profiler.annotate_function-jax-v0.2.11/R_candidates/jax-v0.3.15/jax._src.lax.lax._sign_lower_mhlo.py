def _sign_lower_mhlo(ctx, x):
  x_aval, = ctx.avals_in
  if dtypes.issubdtype(x_aval.dtype, np.unsignedinteger):
    return mhlo.SelectOp(
        mlir.compare_mhlo(x, mlir.full_like_aval(0, x_aval), 'EQ',
                          'UNSIGNED').result,
        mlir.full_like_aval(0, x_aval),
        mlir.full_like_aval(1, x_aval)).results
  return mhlo.SignOp(x).results
