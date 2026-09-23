  def __eq__(self, other):
    if not isinstance(other, SingleDeviceSharding):
      return False
    if self is other:
      return True
    return (self._device == other._device and
            self.memory_kind == other.memory_kind)
