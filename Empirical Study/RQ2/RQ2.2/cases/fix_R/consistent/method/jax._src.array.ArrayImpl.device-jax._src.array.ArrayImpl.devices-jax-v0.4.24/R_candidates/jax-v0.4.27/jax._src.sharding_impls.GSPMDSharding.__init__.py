  @use_cpp_method()
  def __init__(self, devices: Sequence[Device],
               op_sharding: xc.OpSharding | xc.HloSharding,
               *, memory_kind: str | None = None,
               _device_list: xc.DeviceList | None = None):
    self._devices = tuple(devices)
    if isinstance(op_sharding, xc.OpSharding):
      self._hlo_sharding = xc.HloSharding.from_proto(op_sharding)
    else:
      self._hlo_sharding = op_sharding
    self._memory_kind = memory_kind
