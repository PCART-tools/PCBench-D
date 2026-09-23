def eval_dynamic_shape_as_tensor(ctx: LoweringRuleContext,
                                 shape: core.Shape) -> Value:
  """Evaluates the dynamic shapes as one 1d int32 tensor."""
  return shape_tensor(eval_dynamic_shape(ctx, shape))
