def _reduce_or(operand: ArrayLike, axes: Sequence[int]) -> Array:
  return reduce_or_p.bind(operand, axes=tuple(axes))
