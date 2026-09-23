  def __hash__(self) -> int:
    return hash((self.__class__, self._impl))
