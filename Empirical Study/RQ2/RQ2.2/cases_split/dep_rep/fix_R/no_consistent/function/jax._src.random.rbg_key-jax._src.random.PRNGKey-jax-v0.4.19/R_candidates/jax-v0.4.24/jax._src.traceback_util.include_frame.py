def include_frame(f: types.FrameType) -> bool:
  return not any(_path_starts_with(f.f_code.co_filename, path)
                 for path in _exclude_paths)
