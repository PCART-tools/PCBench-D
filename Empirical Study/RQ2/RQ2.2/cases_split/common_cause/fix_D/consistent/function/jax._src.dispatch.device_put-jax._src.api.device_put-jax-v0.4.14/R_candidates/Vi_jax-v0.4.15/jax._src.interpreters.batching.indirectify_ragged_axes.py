def indirectify_ragged_axes(dims):
  if not any(type(d) is RaggedAxis for d in dims):
    return [], dims
  axis_map : dict[int, tuple[Array, pe.DBIdx]] = collections.OrderedDict()
  def canonicalize_segment_lengths(d: RaggedAxis) -> RaggedAxis:
    new_ragged_axes = []
    for ragged_axis, segment_lengths in d.ragged_axes:
      _, dbidx = axis_map.setdefault(
          id(core.get_referent(segment_lengths)),
          (segment_lengths, pe.DBIdx(len(axis_map))))
      new_ragged_axes.append((ragged_axis, dbidx))
    return RaggedAxis(d.stacked_axis, tuple(new_ragged_axes))
  new_dims = [canonicalize_segment_lengths(d)
              if isinstance(d, RaggedAxis) else d for d in dims]
  segment_lens = [s for s, _ in axis_map.values()]
  return segment_lens, new_dims
