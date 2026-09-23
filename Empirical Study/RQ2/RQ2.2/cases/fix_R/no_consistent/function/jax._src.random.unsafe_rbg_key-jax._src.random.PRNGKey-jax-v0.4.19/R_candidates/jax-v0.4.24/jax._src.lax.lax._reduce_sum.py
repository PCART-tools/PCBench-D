def _reduce_sum(operand: ArrayLike, axes: Sequence[int]) -> Array:
  return reduce_sum_p.bind(operand, axes=tuple(axes))
