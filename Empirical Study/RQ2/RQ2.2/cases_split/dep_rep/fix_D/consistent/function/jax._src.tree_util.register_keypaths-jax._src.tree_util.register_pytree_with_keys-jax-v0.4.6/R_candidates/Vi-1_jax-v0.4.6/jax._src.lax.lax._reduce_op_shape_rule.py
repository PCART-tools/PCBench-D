def _reduce_op_shape_rule(operand, *, axes, input_shape=None):
  del input_shape  # Unused.
  if len(axes) != len(set(axes)):
    raise ValueError(f"duplicate value in 'axes' of reduction: {axes}")
  if not all(0 <= a < operand.ndim for a in axes):
    raise ValueError(f"reduction axes {axes} contains out-of-bounds indices for {operand}.")
  axes = frozenset(axes)
  return tuple(d for i, d in enumerate(operand.shape) if i not in axes)
