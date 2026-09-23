  def store(self, val):
    if self._val is not _EMPTY_STORE_VALUE:
      raise StoreException("Store occupied")
    self._val = val
