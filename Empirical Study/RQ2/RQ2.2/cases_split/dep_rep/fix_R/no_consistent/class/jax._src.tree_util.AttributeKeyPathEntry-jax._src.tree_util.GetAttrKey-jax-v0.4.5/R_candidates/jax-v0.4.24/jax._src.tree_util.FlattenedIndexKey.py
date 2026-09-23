@dataclass(frozen=True)
class FlattenedIndexKey():
  key: int
  def __str__(self):
    return f'[<flat index {self.key}>]'
