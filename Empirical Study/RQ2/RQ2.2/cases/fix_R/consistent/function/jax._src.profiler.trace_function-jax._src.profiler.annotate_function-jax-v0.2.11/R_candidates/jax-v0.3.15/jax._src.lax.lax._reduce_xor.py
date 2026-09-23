def _reduce_xor(operand: Array, axes: Sequence[int]) -> Array:
  return reduce_xor_p.bind(operand, axes=tuple(axes))
