@dataclasses.dataclass(frozen=True)
class NameStack:
  stack: Tuple[Union[Scope, Transform], ...] = ()

  def extend(self, name: Union[Tuple[str, ...], str]) -> 'NameStack':
    if not isinstance(name, tuple):
      name = (name,)
    scopes = tuple(map(Scope, name))
    return NameStack(self.stack + scopes)

  def wrap_name(self, name: str) -> str:
    if not self.stack:
      return name
    return f'{str(self)}/{name}'

  def transform(self, transform_name: str) -> 'NameStack':
    return NameStack((*self.stack, Transform(transform_name)))

  def __getitem__(self, idx) -> 'NameStack':
    return NameStack(self.stack[idx])

  def __len__(self):
    return len(self.stack)

  def __add__(self, other: 'NameStack') -> 'NameStack':
    return NameStack(self.stack + other.stack)

  def __radd__(self, other: 'NameStack') -> 'NameStack':
    return NameStack(other.stack + self.stack)

  def __str__(self) -> str:
    scope: Tuple[str, ...] = ()
    for elem in self.stack[::-1]:
      scope = elem.wrap(scope)
    return '/'.join(scope)
