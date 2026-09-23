  def __nonzero__(self):
    return self._val is not _EMPTY_STORE_VALUE
