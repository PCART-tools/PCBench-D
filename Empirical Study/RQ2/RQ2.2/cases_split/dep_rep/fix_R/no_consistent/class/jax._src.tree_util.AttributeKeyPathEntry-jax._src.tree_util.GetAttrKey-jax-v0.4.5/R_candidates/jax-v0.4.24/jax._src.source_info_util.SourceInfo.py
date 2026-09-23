class SourceInfo(NamedTuple):
  traceback: Traceback | None
  name_stack: NameStack

  def replace(self, *, traceback: Traceback | None = None,
      name_stack: NameStack | None = None) -> SourceInfo:
    return SourceInfo(
        self.traceback if traceback is None else traceback,
        self.name_stack if name_stack is None else name_stack
    )
