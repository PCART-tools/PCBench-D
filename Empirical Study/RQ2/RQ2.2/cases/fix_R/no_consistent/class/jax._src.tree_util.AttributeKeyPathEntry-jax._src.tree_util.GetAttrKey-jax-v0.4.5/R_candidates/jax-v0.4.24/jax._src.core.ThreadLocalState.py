class ThreadLocalState(threading.local):
  def __init__(self):
    self.trace_state = TraceState()
