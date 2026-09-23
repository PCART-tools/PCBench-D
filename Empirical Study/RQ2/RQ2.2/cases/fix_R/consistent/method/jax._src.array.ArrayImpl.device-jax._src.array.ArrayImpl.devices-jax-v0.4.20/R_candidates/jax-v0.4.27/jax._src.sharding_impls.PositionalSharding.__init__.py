  def __init__(self, devices: Sequence[xc.Device] | np.ndarray,
               *, memory_kind: str | None = None):
    if xla_extension_version >= 235:
      super().__init__()
    if not isinstance(devices, np.ndarray):
      devices = np.array(devices, dtype='object')
    if not devices.size:
      raise ValueError(f"{self.__class__.__name__}.__init__ requires at least "
                       f"one device, got {devices}")
    self._devices = tuple(devices.flat)
    self._memory_kind = memory_kind
    name = self._devices[0].platform.upper()
    self._ids = np.array([DeviceIdSet(name, i) for i in range(devices.size)],
                         dtype='object').reshape(devices.shape)
    self._internal_device_list = xc.DeviceList(self._devices)
    self._memory_kind = xc.check_and_canonicalize_memory_kind(
        self._memory_kind, self._internal_device_list)
