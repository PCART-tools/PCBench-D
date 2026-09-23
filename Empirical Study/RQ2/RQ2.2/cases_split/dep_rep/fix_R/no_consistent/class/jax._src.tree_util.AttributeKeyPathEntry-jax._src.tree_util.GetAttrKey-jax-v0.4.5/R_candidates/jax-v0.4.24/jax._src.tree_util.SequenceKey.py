@dataclass(frozen=True)
class SequenceKey():
  idx: int
  def __str__(self):
    return f'[{self.idx!r}]'
