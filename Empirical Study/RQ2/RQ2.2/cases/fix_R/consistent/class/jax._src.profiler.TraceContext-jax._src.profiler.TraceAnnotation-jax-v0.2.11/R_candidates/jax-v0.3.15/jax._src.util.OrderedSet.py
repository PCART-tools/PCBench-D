class OrderedSet(Generic[T]):
  elts_set: Set[T]
  elts_list: List[T]

  def __init__(self):
    self.elts_set = set()
    self.elts_list = []

  def add(self, elt: T) -> None:
    if elt not in self.elts_set:
      self.elts_set.add(elt)
      self.elts_list.append(elt)

  def update(self, elts: Seq[T]) -> None:
    for e in elts:
      self.add(e)

  def __iter__(self) -> Iterator[T]:
    return iter(self.elts_list)

  def __len__(self) -> int:
    return len(self.elts_list)

  def __contains__(self, elt: T) -> bool:
    return elt in self.elts_set
