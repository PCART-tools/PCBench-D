class Scope(NamedTuple):
  name: str

  def wrap(self, stack: Tuple[str, ...]) -> Tuple[str, ...]:
    return (self.name, *stack)
