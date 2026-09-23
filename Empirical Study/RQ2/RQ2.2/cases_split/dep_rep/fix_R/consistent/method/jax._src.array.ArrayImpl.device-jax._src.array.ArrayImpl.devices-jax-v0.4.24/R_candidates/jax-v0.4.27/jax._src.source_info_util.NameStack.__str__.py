  def __str__(self) -> str:
    scope: tuple[str, ...] = ()
    for elem in self.stack[::-1]:
      scope = elem.wrap(scope)
    return '/'.join(scope)
