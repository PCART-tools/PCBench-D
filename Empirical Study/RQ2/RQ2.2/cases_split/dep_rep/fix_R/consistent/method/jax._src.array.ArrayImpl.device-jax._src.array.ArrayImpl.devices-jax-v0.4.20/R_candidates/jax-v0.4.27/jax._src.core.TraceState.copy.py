  def copy(self):
    new = self.__new__(TraceState)
    new.trace_stack = self.trace_stack.copy()
    new.substack = self.substack[:]
    new.axis_env = self.axis_env[:]
    return new
