class Transform(NamedTuple):
  name: str

  def wrap(self, stack: tuple[str, ...]) -> tuple[str, ...]:
    if stack:
      return (f'{self.name}({stack[0]})', *stack[1:])
    else:
      return ()
