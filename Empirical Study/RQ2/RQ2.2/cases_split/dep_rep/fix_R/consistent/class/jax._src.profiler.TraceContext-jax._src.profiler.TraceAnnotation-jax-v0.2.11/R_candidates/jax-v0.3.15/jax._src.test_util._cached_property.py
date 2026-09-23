class _cached_property:
  null = object()

  def __init__(self, method):
    self._method = method
    self._value = self.null

  def __get__(self, obj, cls):
    if self._value is self.null:
      self._value = self._method(obj)
    return self._value
