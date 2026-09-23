  def __reduce__(self):
    return type(self), (self._device,), {'memory_kind': self._memory_kind}
