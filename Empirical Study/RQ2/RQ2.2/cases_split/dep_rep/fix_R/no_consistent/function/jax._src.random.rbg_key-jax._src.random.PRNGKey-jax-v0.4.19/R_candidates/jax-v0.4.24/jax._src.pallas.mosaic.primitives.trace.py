@contextlib.contextmanager
def trace(message: str, level: int = 10):
  trace_start_p.bind(message=message, level=level)
  yield
  trace_stop_p.bind()
