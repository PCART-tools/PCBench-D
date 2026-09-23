@dataclass(frozen=True)
class GetAttrKey():
  name: str
  def __str__(self):
    return f'.{self.name}'
