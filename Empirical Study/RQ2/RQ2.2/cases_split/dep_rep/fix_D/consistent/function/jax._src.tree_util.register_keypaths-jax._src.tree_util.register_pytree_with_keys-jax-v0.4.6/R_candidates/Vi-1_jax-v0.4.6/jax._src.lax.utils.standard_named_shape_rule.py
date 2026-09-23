def standard_named_shape_rule(*avals, **kwargs):
  return core.join_named_shapes(*(a.named_shape for a in avals))
