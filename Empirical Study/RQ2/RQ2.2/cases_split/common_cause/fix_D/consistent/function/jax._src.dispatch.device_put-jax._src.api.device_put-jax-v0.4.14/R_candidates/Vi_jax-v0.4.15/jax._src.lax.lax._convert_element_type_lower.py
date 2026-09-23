def _convert_element_type_lower(ctx, operand, *, new_dtype, weak_type):
  aval_in, = ctx.avals_in
  aval_out, = ctx.avals_out
  if (dtypes.issubdtype(aval_in.dtype, np.complexfloating) and
      not dtypes.issubdtype(new_dtype, np.complexfloating)):
    operand = hlo.RealOp(operand).result
    aval_in = aval_in.update(dtype=_real_dtype(aval_in.dtype))
  return [mlir.convert_hlo(ctx, operand, aval_in, aval_out)]
