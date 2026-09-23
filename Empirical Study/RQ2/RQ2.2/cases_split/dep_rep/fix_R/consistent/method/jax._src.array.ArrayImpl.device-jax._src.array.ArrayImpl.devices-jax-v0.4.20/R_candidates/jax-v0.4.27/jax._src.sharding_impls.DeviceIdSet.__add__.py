  def __add__(self, other) -> DeviceIdSet:
    assert isinstance(other, DeviceIdSet)
    return DeviceIdSet(self._name, *(self._ids | other._ids))
