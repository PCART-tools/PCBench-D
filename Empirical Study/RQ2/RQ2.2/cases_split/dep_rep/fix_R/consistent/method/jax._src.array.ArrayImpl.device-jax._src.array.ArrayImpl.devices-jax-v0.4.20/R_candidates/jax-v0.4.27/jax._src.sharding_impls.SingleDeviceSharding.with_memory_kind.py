  def with_memory_kind(self, kind: str) -> SingleDeviceSharding:
    return SingleDeviceSharding(self._device, memory_kind=kind)
