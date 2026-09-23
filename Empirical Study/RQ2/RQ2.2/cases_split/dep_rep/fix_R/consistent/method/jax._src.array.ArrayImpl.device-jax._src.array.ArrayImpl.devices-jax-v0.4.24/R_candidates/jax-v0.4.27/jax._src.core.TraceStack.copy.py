  def copy(self):
    new = self.__new__(TraceStack)
    new.stack = self.stack[:]
    new.dynamic = self.dynamic
    return new
