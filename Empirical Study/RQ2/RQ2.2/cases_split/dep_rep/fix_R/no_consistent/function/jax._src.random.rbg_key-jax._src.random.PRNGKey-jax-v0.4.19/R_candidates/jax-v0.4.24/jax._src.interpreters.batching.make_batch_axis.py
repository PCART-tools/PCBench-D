def make_batch_axis(
    ndim: int,
    stacked_axis: int,
    ragged_axes: list[tuple[int, Array | core.Var]],
) -> int | RaggedAxis:
  if ragged_axes:
    canonical = [(canonicalize_axis(ax, ndim), sz) for ax, sz in ragged_axes]
    return _sorted_ragged_axis(canonicalize_axis(stacked_axis, ndim), canonical)
  else:
    return canonicalize_axis(stacked_axis, ndim)
