  def wrap(self, stack: tuple[str, ...]) -> tuple[str, ...]:
    return (self.name, *stack)
