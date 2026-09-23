def _reduce_min(operand: ArrayLike, axes: Sequence[int]) -> Array:
  return reduce_min_p.bind(operand, axes=tuple(axes))
