def multi_broadcast_in_dim(ctx: LoweringRuleContext,
                           ops: Sequence[ir.Value],
                           ops_avals: Sequence[core.AbstractValue],
                           out_shape: core.Shape) -> Sequence[ir.Value]:
  """Broadcasts multiple ops to the out_shape."""
  out = []
  for op, op_aval in zip(ops, ops_avals):
    op_aval_shape = op_aval.shape  # type: ignore
    if core.symbolic_equal_shape(op_aval_shape, out_shape):  # type: ignore
      out.append(op)
    else:
      assert len(op_aval_shape) <= len(out_shape), (op_aval_shape, out_shape)
      broadcast_dimensions = list(range(len(out_shape) - len(op_aval_shape), len(out_shape)))
      out.append(broadcast_in_dim(ctx, op,
                                  core.ShapedArray(out_shape, op_aval.dtype),  # type: ignore
                                  broadcast_dimensions=broadcast_dimensions))
  return out
