  def __repr__(self):
    mem = '' if self._memory_kind is None else f', memory_kind={self._memory_kind}'
    return f"SingleDeviceSharding(device={self._device!r}{mem})"
