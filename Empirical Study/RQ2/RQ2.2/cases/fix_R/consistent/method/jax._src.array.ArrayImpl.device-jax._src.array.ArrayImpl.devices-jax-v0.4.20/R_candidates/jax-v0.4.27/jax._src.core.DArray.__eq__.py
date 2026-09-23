  def __eq__(self, other):
    if isinstance(other, DArray) and self._aval == other._aval:
      return self._data == other._data
    return False
