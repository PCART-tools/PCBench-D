def _source_info_to_location(
    ctx: ModuleContext, primitive: core.Primitive, params: dict[str, Any],
    source_info: source_info_util.SourceInfo) -> ir.Location:
  eqn_str = (f'{source_info.name_stack}/'
             f'{core.str_eqn_compact(primitive.name, params)}')
  if config.include_full_tracebacks_in_locations.value:
    if source_info.traceback is None:
      loc = ir.Location.unknown()
    else:
      loc = _traceback_to_location(ctx, source_info.traceback)
  else:
    frame = source_info_util.user_frame(source_info)
    if frame is None:
      loc = ir.Location.unknown()
    else:
      loc = ir.Location.file(get_canonical_source_file(frame.file_name,
                                                       ctx.traceback_caches),
                             frame.start_line, frame.start_column)
  loc = ir.Location.name(eqn_str, childLoc=loc)
  # TODO(phawkins): also include primitive.name as the operator type.
  return loc
