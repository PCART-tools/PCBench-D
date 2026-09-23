def indirectify_ragged_axes_against_inputs_outputs(dims, in_vals, out_vals):
  def canonicalize_segment_lengths(d: RaggedAxis) -> RaggedAxis:
    new_ragged_axes = []
    for ragged_axis, segment_lengths in d.ragged_axes:
      key = id(core.get_referent(segment_lengths))
      value = _locate_value(key, in_vals, out_vals)
      new_ragged_axes.append((ragged_axis, value))
    return RaggedAxis(d.stacked_axis, tuple(new_ragged_axes))
  new_dims = [canonicalize_segment_lengths(d)
              if isinstance(d, RaggedAxis) else d for d in dims]
  return new_dims
