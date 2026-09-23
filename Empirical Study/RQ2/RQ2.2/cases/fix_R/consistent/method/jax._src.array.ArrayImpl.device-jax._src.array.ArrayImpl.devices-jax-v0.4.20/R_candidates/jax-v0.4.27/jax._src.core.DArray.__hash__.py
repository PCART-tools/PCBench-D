  def __hash__(self) -> int:
    if not self.shape:
      return hash((self._aval, int(self._data)))
    raise TypeError("unhashable type: DArray")
