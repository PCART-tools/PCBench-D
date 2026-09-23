def _reduce_xor(operand: ArrayLike, axes: Sequence[int]) -> Array:
  return reduce_xor_p.bind(operand, axes=tuple(axes))
