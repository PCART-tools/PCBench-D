  def __getitem__(self, idx: slice) -> NameStack:
    return NameStack(self.stack[idx])
