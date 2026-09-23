@functools.lru_cache(maxsize=64)
def user_frame(source_info: SourceInfo) -> Optional[Frame]:
  return next(user_frames(source_info), None)
