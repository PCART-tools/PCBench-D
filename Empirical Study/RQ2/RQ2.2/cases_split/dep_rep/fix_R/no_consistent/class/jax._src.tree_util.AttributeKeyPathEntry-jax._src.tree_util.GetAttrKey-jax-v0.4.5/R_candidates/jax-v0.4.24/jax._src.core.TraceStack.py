class TraceStack:
  # See comments in https://github.com/google/jax/pull/3370
  stack: list[MainTrace]
  dynamic: MainTrace

  def __init__(self):
    eval_trace = MainTrace(0, EvalTrace)
    self.stack = [eval_trace]
    self.dynamic = eval_trace

  def next_level(self) -> int:
    return len(self.stack)

  def push(self, main_trace: MainTrace) -> None:
    self.stack.append(main_trace)

  def pop(self) -> None:
    self.stack.pop()

  def __repr__(self) -> str:
    stack_str = map('  {}\n'.format, self.stack[::-1])
    return f'Trace stack\n{stack_str}\n{self.dynamic}'

  def copy(self):
    new = self.__new__(TraceStack)
    new.stack = self.stack[:]
    new.dynamic = self.dynamic
    return new
