def _traceback_to_location(ctx: ModuleContext, tb: xc.Traceback) -> ir.Location:
  """Converts a full traceback to a callsite() MLIR location."""
  frame_locs = []
  frames_limit = config.traceback_in_locations_limit.value
  if frames_limit == 0:
    return ir.Location.unknown()

  for code, lasti in zip(*tb.raw_frames()):
    if not _is_user_file(ctx, code.co_filename):
      continue

    frame = _raw_frame_to_frame(ctx, code, lasti)
    file_loc = ir.Location.file(
        get_canonical_source_file(frame.file_name, ctx.traceback_caches),
        frame.start_line,
        frame.start_column,
    )
    name_loc = ir.Location.name(frame.function_name, childLoc=file_loc)
    frame_locs.append(name_loc)
    if frames_limit > 0 and len(frame_locs) >= frames_limit:
      break

  if len(frame_locs) == 0:
    return ir.Location.unknown()
  else:
    if len(frame_locs) == 1:
      return frame_locs[0]

    return ir.Location.callsite(frame_locs[0], frame_locs[1:])
