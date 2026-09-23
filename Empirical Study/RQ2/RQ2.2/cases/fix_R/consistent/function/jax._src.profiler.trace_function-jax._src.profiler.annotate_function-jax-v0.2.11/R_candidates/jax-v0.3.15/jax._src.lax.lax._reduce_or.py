def _reduce_or(operand: Array, axes: Sequence[int]) -> Array:
  return reduce_or_p.bind(operand, axes=tuple(axes))
