def slice(operand: ArrayLike, start_indices: Sequence[int],
          limit_indices: Sequence[int],
          strides: Optional[Sequence[int]] = None) -> Array:
  """Wraps XLA's `Slice
  <https://www.tensorflow.org/xla/operation_semantics#slice>`_
  operator.
  """
  return slice_p.bind(operand, start_indices=tuple(start_indices),
                      limit_indices=tuple(limit_indices),
                      strides=None if strides is None else tuple(strides))
