@functools.lru_cache(maxsize=64)
def user_frame(source_info: SourceInfo) -> Frame | None:
  return next(user_frames(source_info), None)
