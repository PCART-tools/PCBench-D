@dataclasses.dataclass(frozen=True)
class IgnoreKey:
  val: Any
  def __hash__(self):
    return hash(self.__class__)
  def __eq__(self, other):
    return isinstance(other, IgnoreKey)  # ignore self.val!
