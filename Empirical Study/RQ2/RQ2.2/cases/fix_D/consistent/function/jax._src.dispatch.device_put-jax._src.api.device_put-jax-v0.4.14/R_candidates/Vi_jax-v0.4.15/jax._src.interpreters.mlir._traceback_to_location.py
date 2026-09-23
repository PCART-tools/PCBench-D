def _traceback_to_location(tb: xc.Traceback) -> ir.Location:
  """Converts a full traceback to a callsite() MLIR location."""
  frame_locs = []
  for code, lasti in zip(*tb.raw_frames()):
    frame = source_info_util.raw_frame_to_frame(code, lasti)
    if source_info_util.is_user_filename(frame.file_name):
      file_loc = ir.Location.file(
          get_canonical_source_file(frame),
          frame.start_line,
          frame.start_column,
      )
      name_loc = ir.Location.name(frame.function_name, childLoc=file_loc)
      frame_locs.append(name_loc)

  if len(frame_locs) == 0:
    return ir.Location.unknown()
  else:
    if len(frame_locs) == 1:
      return frame_locs[0]

    return ir.Location.callsite(frame_locs[0], frame_locs[1:])
