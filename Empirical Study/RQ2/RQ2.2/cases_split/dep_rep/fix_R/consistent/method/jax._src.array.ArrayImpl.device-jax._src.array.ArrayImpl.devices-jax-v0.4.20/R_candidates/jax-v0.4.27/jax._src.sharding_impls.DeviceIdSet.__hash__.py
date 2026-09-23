  def __hash__(self) -> int:
    return hash((self._name, self._ids))
