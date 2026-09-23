  @classmethod
  def from_frameinfo(cls, frame_info) -> DebuggerFrame:
    try:
      _, start = inspect.getsourcelines(frame_info.frame)
      source = inspect.getsource(frame_info.frame).split("\n")
      # Line numbers begin at 1 but offsets begin at 0. `inspect.getsource` will
      # return a partial view of the file and a `start` indicating the line
      # number that the source code starts at. However, it's possible that
      # `start` is 0, indicating that we are at the beginning of the file. In
      # this case, `offset` is just the `lineno - 1`. If `start` is nonzero,
      # then we subtract it off from the `lineno` and don't need to subtract 1
      # since both start and lineno are 1-indexed.
      offset = frame_info.lineno - max(start, 1)
    except OSError:
      source = []
      offset = None
    return DebuggerFrame(
        filename=frame_info.filename,
        locals=frame_info.frame.f_locals,
        globals={},
        code_context=frame_info.code_context,
        source=source,
        lineno=frame_info.lineno,
        offset=offset)
