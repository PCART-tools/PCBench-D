  @property
  def val(self):
    if not self:
      raise StoreException("Store empty")
    return self._val
