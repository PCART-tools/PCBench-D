class StoreEqual(lu.Store):
  """Stores an unchanging value. Checks empty reads and unequal overwrites."""
  def store(self, val):
    if self._val is not lu._EMPTY_STORE_VALUE and val != self._val:
      raise lu.StoreException(
          f"Store assignment mismatch, from {self._val} to {val}")
    self._val = val
