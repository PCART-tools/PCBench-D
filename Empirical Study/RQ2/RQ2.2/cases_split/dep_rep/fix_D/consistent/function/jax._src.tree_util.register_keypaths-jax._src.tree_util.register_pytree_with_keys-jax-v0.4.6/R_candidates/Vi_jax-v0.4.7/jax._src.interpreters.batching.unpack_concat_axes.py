def unpack_concat_axes(dims):
  if not any(type(d) is ConcatAxis for d in dims):
    return [], dims
  concat_axis_map = collections.OrderedDict()
  def convert(d: ConcatAxis) -> ConcatAxis:
    _, dbidx = concat_axis_map.setdefault(
        id(core.get_referent(d.segment_lengths)),
        (d.segment_lengths, pe.DBIdx(len(concat_axis_map))))
    return ConcatAxis(d.axis, dbidx)
  new_dims = [convert(d) if isinstance(d, ConcatAxis) else d for d in dims]
  segment_lens = [s for s, _ in concat_axis_map.values()]
  return segment_lens, new_dims
