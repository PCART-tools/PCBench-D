def _reduce_sum(operand: Array, axes: Sequence[int]) -> Array:
  return reduce_sum_p.bind(operand, axes=tuple(axes))
