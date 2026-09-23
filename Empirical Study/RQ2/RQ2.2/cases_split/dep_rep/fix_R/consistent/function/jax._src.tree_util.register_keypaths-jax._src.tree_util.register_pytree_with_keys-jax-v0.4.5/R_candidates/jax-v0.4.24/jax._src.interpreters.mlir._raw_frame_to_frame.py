def _raw_frame_to_frame(ctx: ModuleContext,
                        code: source_info_util.types.CodeType, lasti: int):
  key = (code.co_filename, lasti)
  if key in ctx.traceback_caches.raw_frame_to_frame_cache:
    return ctx.traceback_caches.raw_frame_to_frame_cache[key]
  frame = source_info_util.raw_frame_to_frame(code, lasti)
  ctx.traceback_caches.raw_frame_to_frame_cache[key] = frame
  return frame
