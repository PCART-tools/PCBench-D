def _reduce_min(operand: Array, axes: Sequence[int]) -> Array:
  return reduce_min_p.bind(operand, axes=tuple(axes))
