  def __hash__(self):
    if not hasattr(self, '_hash'):
      self._hash = hash((self._device, self.memory_kind))
    return self._hash
