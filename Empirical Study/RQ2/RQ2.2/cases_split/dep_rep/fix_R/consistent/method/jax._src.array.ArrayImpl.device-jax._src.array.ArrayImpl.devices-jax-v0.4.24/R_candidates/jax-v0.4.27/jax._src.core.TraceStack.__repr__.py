  def __repr__(self) -> str:
    stack_str = map('  {}\n'.format, self.stack[::-1])
    return f'Trace stack\n{stack_str}\n{self.dynamic}'
