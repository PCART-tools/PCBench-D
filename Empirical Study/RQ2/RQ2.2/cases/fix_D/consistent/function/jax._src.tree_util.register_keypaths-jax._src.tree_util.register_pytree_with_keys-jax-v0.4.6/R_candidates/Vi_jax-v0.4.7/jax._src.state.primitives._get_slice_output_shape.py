def _get_slice_output_shape(in_shape: Tuple[int, ...],
                            idx_shapes: Tuple[Tuple[int, ...], ...],
                            indexed_dims: Tuple[bool, ...]) -> Tuple[int, ...]:
  shape_suffix = [d for i, d in zip(indexed_dims, in_shape) if not i]
  shape_prefix, = set(idx_shapes) or [()]  # tie fighter
  # Move shape prefix dimensions to the front
  shape = (*shape_prefix, *shape_suffix)
  return shape
