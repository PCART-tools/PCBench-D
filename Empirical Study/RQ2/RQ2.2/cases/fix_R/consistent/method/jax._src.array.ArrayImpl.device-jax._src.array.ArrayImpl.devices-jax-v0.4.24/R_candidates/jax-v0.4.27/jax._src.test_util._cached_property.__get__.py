  def __get__(self, obj, cls):
    if self._value is self.null:
      self._value = self._method(obj)
    return self._value
