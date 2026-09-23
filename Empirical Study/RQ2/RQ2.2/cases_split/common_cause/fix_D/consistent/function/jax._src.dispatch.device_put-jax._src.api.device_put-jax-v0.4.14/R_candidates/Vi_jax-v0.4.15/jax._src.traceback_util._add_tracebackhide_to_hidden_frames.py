def _add_tracebackhide_to_hidden_frames(tb: types.TracebackType):
  for f, _lineno in traceback.walk_tb(tb):
    if not include_frame(f):
      f.f_locals["__tracebackhide__"] = True
