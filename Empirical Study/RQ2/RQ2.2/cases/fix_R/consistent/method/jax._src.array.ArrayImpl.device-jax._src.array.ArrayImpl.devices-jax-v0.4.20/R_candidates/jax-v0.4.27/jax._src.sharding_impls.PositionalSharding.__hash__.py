  def __hash__(self) -> int:
    if not hasattr(self, '_hash'):
      self._hash = hash((self._internal_device_list, self.memory_kind))
    return self._hash
