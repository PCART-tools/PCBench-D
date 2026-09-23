def _reduce_and(operand: ArrayLike, axes: Sequence[int]) -> Array:
  return reduce_and_p.bind(operand, axes=tuple(axes))
