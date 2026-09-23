def _reduce_max(operand: Array, axes: Sequence[int]) -> Array:
  return reduce_max_p.bind(operand, axes=tuple(axes))
