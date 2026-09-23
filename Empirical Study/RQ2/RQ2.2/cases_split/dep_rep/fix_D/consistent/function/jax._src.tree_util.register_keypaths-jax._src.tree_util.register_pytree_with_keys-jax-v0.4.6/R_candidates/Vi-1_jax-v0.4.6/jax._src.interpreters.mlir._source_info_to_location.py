def _source_info_to_location(
    primitive: core.Primitive, params: Dict,
    source_info: source_info_util.SourceInfo,
    name_stack: source_info_util.NameStack) -> ir.Location:
  eqn_str = (f'{str(source_info.name_stack)}/'
             f'{core.str_eqn_compact(primitive.name, params)}')
  frame = source_info_util.user_frame(source_info)
  if frame is None:
    loc = ir.Location.unknown()
  else:
    loc = ir.Location.file(xla.get_canonical_source_file(frame),
                           frame.start_line, frame.start_column)
  loc = ir.Location.name(eqn_str, childLoc=loc)
  # TODO(phawkins): also include primitive.name as the operator type.
  return loc
