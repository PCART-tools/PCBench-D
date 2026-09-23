def transpose_ragged_axes(dim: RaggedAxis, perm: tuple[int, ...]) -> RaggedAxis:
  new_ragged_axes = []
  for idx, old_idx in enumerate(perm):
    for ax, size in dim.ragged_axes:
      if old_idx == ax:
        new_ragged_axes.append((idx, size))
        break
  return _sorted_ragged_axis(dim.stacked_axis, new_ragged_axes)
