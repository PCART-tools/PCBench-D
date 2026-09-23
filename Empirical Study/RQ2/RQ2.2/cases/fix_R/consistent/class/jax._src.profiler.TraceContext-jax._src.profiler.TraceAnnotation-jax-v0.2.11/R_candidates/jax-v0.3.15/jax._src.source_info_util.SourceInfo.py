class SourceInfo(NamedTuple):
  traceback: Optional[Traceback]
  name_stack: NameStack

  def replace(self, *, traceback: Optional[Traceback] = None,
      name_stack: Optional[NameStack] = None) -> 'SourceInfo':
    traceback = traceback or self.traceback
    name_stack = self.name_stack if name_stack is None else name_stack
    return self._replace(traceback=traceback, name_stack=name_stack)
