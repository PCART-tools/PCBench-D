def mask_ragged_axes(operand: Array, ident, axis_spec: RaggedAxis) -> Array:
  # TODO(mattjj, axch) Can we mask multiple axes more efficiently at
  # once, rather than one at a time?
  for ragged_axis, segment_lengths in axis_spec.ragged_axes:
    this_axis_spec = RaggedAxis(
        axis_spec.stacked_axis, ((ragged_axis, segment_lengths),))
    operand = _mask_one_ragged_axis(operand, ident, this_axis_spec)
  return operand
