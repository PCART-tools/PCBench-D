class KeyPath(NamedTuple):
  keys: Tuple[KeyPathEntry, ...]
  def __add__(self, other):
    if isinstance(other, KeyPathEntry):
      return KeyPath(self.keys + (other,))
    raise TypeError(type(other))
  def pprint(self) -> str:
    if not self.keys:
      return ' tree root'
    return ''.join(k.pprint() for k in self.keys)
