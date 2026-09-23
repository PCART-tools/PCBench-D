def _reduce_prod(operand: ArrayLike, axes: Sequence[int]) -> Array:
  return reduce_prod_p.bind(operand, axes=tuple(axes))
