@dataclass(frozen=True)
class DictKey():
  key: Hashable
  def __str__(self):
    return f'[{self.key!r}]'
