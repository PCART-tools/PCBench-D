def concrete_dim_or_error(val: Any, context=""):
  """Like concrete_or_error(operator.index)."""
  if is_dim(val):
    return val
  else:
    return concrete_or_error(operator.index, val, context=context)
