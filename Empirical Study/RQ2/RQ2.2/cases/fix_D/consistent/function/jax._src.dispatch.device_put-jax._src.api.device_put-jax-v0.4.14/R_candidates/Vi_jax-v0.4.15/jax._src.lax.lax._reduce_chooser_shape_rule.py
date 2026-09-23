def _reduce_chooser_shape_rule(operand, *, axes):
  return tuple(np.delete(operand.shape, axes))
