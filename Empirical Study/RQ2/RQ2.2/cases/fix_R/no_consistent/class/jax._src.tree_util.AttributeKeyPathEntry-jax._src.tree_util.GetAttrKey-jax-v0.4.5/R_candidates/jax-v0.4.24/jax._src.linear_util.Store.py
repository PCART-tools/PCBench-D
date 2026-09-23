class Store:
  """Storage for a value, with checks for overwriting or reading empty store."""
  __slots__ = ("_val",)

  def __init__(self):
    self._val = _EMPTY_STORE_VALUE

  def store(self, val):
    if self._val is not _EMPTY_STORE_VALUE:
      raise StoreException("Store occupied")
    self._val = val

  def reset(self):
    # This should only be called in exceptional circumstances (e.g. debugging).
    self._val = _EMPTY_STORE_VALUE

  @property
  def val(self):
    if not self:
      raise StoreException("Store empty")
    return self._val

  def __nonzero__(self):
    return self._val is not _EMPTY_STORE_VALUE

  __bool__ = __nonzero__
