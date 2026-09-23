def sort(operand: Union[Array, Sequence[Array]], dimension: int = -1,
         is_stable: bool = True, num_keys: int = 1) -> Union[Array, tuple[Array, ...]]:
  """Wraps XLA's `Sort
  <https://www.tensorflow.org/xla/operation_semantics#sort>`_ operator.

  For floating point inputs, -0.0 and 0.0 are treated as equivalent, and NaN values
  are sorted to the end of the array. For complex inputs, the sort order is
  lexicographic over the real and imaginary parts, with the real part primary.

  Args:
    operand : Array or sequence of arrays
    dimension : integer dimension along which to sort. Default: -1.
    is_stable : boolean specifying whether to use a stable sort. Default: True.
    num_keys : number of operands to treat as sort keys. Default: 1.
      For num_keys > 1, the sort order will be determined lexicographically using
      the first `num_keys` arrays, with the first key being primary.
      The remaining operands will be returned with the same permutation.

  Returns:
    operand : sorted version of the input or inputs.
  """
  if isinstance(operand, Sequence):
    if len(operand) == 0:
      raise TypeError("Sort requires at least one operand")
    if not (1 <= num_keys <= len(operand)):
      raise ValueError(f"{num_keys=} must be between 1 and {len(operand)=}")
    dimension = canonicalize_axis(dimension, len(operand[0].shape))
    return tuple(sort_p.bind(*operand, dimension=dimension,
                             is_stable=is_stable,
                             num_keys=num_keys))
  else:
    if num_keys != 1:
      raise ValueError(f"{num_keys=} must equal 1 for a single operand.")
    dimension = canonicalize_axis(dimension, len(operand.shape))
    return sort_p.bind(operand, dimension=dimension, is_stable=is_stable, num_keys=1)[0]
