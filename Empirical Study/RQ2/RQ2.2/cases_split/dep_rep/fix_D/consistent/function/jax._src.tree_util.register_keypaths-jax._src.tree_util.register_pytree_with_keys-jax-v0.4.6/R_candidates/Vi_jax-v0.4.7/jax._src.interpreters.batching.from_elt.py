def from_elt(trace: 'BatchTrace', axis_size: AxisSize, x: Elt, spec: MapSpec
             ) -> Vmappable:
  handler = from_elt_handlers.get(type(x))
  if handler:
    return handler(partial(from_elt, trace), axis_size, x, spec)
  x_ = trace.full_raise(x)
  val, bdim = x_.val, x_.batch_dim
  if type(bdim) is ConcatAxis:
    if spec is not pile_axis:
      # TODO(mattjj): improve this error message
      raise TypeError("ragged output without using pile_axis out_axes spec")
    return _pile_result(axis_size, bdim.axis, bdim.segment_lengths, val)
  else:
    return matchaxis(trace.axis_name, axis_size, x_.batch_dim, spec, x_.val)
