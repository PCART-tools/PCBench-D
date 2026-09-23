def _slice_lowering_rule(
    ctx: LoweringRuleContext, x, limit_indices, start_indices, strides
):
  """Lowers a slice to vector dialect."""
  (aval_out,) = ctx.avals_out
  if strides is None:
    strides = [1] * len(start_indices)
  sizes = np.array(limit_indices) - np.array(start_indices)
  op = vector.ExtractStridedSliceOp(
      aval_to_ir_type(aval_out), x, start_indices, sizes, strides
  )
  return op.result
