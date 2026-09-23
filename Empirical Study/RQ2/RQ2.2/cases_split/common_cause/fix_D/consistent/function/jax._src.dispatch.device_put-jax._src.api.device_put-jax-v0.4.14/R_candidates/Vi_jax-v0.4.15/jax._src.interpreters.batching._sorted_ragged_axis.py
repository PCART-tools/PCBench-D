def _sorted_ragged_axis(stacked_axis, ragged_axes):
  return RaggedAxis(stacked_axis, tuple(sorted(ragged_axes, key=lambda p: p[0])))
