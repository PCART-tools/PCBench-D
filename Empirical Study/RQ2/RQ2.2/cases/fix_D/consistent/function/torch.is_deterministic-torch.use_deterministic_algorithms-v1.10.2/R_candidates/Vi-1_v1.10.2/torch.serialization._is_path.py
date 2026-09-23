def _is_path(name_or_buffer):
    return isinstance(name_or_buffer, str) or \
        isinstance(name_or_buffer, pathlib.Path)
