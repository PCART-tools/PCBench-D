class TraceState:
  trace_stack: TraceStack
  substack: list[Sublevel]
  axis_env: list[AxisEnvFrame]

  def __init__(self) -> None:
    self.trace_stack = TraceStack()
    self.substack = [Sublevel(0)]
    self.axis_env = []

  def copy(self):
    new = self.__new__(TraceState)
    new.trace_stack = self.trace_stack.copy()
    new.substack = self.substack[:]
    new.axis_env = self.axis_env[:]
    return new
