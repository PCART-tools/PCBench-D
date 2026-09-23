def _reduce_max(operand: ArrayLike, axes: Sequence[int]) -> Array:
  return reduce_max_p.bind(operand, axes=tuple(axes))
