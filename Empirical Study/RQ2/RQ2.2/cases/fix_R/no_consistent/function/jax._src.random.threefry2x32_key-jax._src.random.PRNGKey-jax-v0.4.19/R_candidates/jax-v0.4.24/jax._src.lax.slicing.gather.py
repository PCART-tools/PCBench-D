def gather(operand: ArrayLike, start_indices: ArrayLike,
           dimension_numbers: GatherDimensionNumbers,
           slice_sizes: Shape,
           *,
           unique_indices: bool = False,
           indices_are_sorted: bool = False,
           mode: str | GatherScatterMode | None = None,
           fill_value = None) -> Array:
  """Gather operator.

  Wraps `XLA's Gather operator
  <https://www.tensorflow.org/xla/operation_semantics#gather>`_.

  The semantics of gather are complicated, and its API might change in the
  future. For most use cases, you should prefer `Numpy-style indexing
  <https://numpy.org/doc/stable/reference/arrays.indexing.html>`_
  (e.g., `x[:, (1,4,7), ...]`), rather than using `gather` directly.

  Args:
    operand: an array from which slices should be taken
    start_indices: the indices at which slices should be taken
    dimension_numbers: a `lax.GatherDimensionNumbers` object that describes
      how dimensions of `operand`, `start_indices` and the output relate.
    slice_sizes: the size of each slice. Must be a sequence of non-negative
      integers with length equal to `ndim(operand)`.
    indices_are_sorted: whether `indices` is known to be sorted. If
      true, may improve performance on some backends.
    unique_indices: whether the elements gathered from ``operand`` are
      guaranteed not to overlap with each other. If ``True``, this may improve
      performance on some backends. JAX does not check this promise: if
      the elements overlap the behavior is undefined.
    mode: how to handle indices that are out of bounds: when set to ``'clip'``,
      indices are clamped so that the slice is within bounds, and when
      set to ``'fill'`` or ``'drop'`` gather returns a slice full of
      ``fill_value`` for the affected slice. The behavior for out-of-bounds
      indices when set to ``'promise_in_bounds'`` is implementation-defined.
    fill_value: the fill value to return for out-of-bounds slices when `mode`
      is ``'fill'``. Ignored otherwise. Defaults to ``NaN`` for inexact types,
      the largest negative value for signed types, the largest positive value
      for unsigned types, and ``True`` for booleans.

  Returns:
    An array containing the gather output.
  """
  if mode is None:
    mode = GatherScatterMode.PROMISE_IN_BOUNDS
  parsed_mode = GatherScatterMode.from_any(mode)
  if parsed_mode == GatherScatterMode.FILL_OR_DROP:
    if fill_value is None:
      dtype = _dtype(operand)
      if dtypes.issubdtype(dtype, np.inexact):
        fill_value = np.nan
      elif dtypes.issubdtype(dtype, np.signedinteger):
        fill_value = dtypes.iinfo(dtype).min
      elif dtypes.issubdtype(dtype, np.unsignedinteger):
        fill_value = dtypes.iinfo(dtype).max
      elif dtype == dtypes.bool_:
        fill_value = True
      else:
        raise ValueError(f"Unsupported dtype for gather fill_value {dtype}")
  else:
    fill_value = None
  return gather_p.bind(
      operand, start_indices, dimension_numbers=dimension_numbers,
      slice_sizes=core.canonicalize_shape(slice_sizes),
      unique_indices=bool(unique_indices),
      indices_are_sorted=bool(indices_are_sorted),
      mode=parsed_mode,
      fill_value=fill_value)
