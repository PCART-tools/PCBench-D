  def extend(self, name: tuple[str, ...] | str) -> NameStack:
    if not isinstance(name, tuple):
      name = (name,)
    scopes = tuple(map(Scope, name))
    return NameStack(self.stack + scopes)
