def include_frame(f):
  return not any(path_starts_with(f.f_code.co_filename, path)
                 for path in _exclude_paths)
