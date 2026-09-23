def pad(operand: ArrayLike, padding_value: ArrayLike,
        padding_config: Sequence[tuple[int, int, int]]) -> Array:
  """Applies low, high, and/or interior padding to an array.

  Wraps XLA's `Pad
  <https://www.tensorflow.org/xla/operation_semantics#pad>`_
  operator.

  Args:
    operand: an array to be padded.
    padding_value: the value to be inserted as padding. Must have the same dtype
      as ``operand``.
    padding_config: a sequence of ``(low, high, interior)`` tuples of integers,
      giving the amount of low, high, and interior (dilation) padding to insert
      in each dimension.

  Returns:
    The ``operand`` array with padding value ``padding_value`` inserted in each
    dimension according to the ``padding_config``.
  """
  return pad_p.bind(operand, padding_value, padding_config=tuple(padding_config))
