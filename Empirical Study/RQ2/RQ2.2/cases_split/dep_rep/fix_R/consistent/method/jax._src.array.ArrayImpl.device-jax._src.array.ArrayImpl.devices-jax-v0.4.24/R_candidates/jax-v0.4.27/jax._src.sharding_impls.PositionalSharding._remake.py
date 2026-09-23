  @classmethod
  def _remake(
      cls, devices: tuple[xc.Device, ...], ids: np.ndarray,
      *, memory_kind: str | None = None) -> PositionalSharding:
    self = cls.__new__(cls)
    self._devices = devices
    self._ids = ids
    self._internal_device_list = xc.DeviceList(self._devices)
    self._memory_kind = xc.check_and_canonicalize_memory_kind(
        memory_kind, self._internal_device_list)
    return self
