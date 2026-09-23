def _reduce_logical_shape_rule(operand, *, axes):
  if operand.dtype != np.bool_:
    msg = "logical reduction requires operand dtype bool, got {}."
    raise TypeError(msg.format(operand.dtype))
  return tuple(np.delete(operand.shape, axes))
