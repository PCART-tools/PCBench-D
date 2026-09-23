@use_cpp_class(xc.GSPMDSharding)
class GSPMDSharding(XLACompatibleSharding):
  _devices: tuple[Device, ...]
  _hlo_sharding: xc.HloSharding
  _memory_kind: str | None
  _device_list: xc.DeviceList | None

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

  def __reduce__(self):
    return (type(self), (self._devices, self._hlo_sharding.to_proto()),
            {'memory_kind': self._memory_kind})

  @functools.cached_property
  def _hlo_sharding_hash(self):
    return hash(self._hlo_sharding)

  def __eq__(self, other):
    if not isinstance(other, GSPMDSharding):
      return False
    if id(self) == id(other):
      return True
    return (are_op_shardings_equal(self._hlo_sharding, other._hlo_sharding)
            and self.memory_kind == other.memory_kind
            and self._internal_device_list == other._internal_device_list)  # type: ignore

  def __hash__(self):
    if not hasattr(self, '_hash'):
      self._hash = hash((self._internal_device_list, self._hlo_sharding_hash,  # type: ignore
                        self.memory_kind))
    return self._hash

  def __repr__(self):
    mem = '' if self._memory_kind is None else f', memory_kind={self._memory_kind}'
    return f'GSPMDSharding({self._hlo_sharding!r}{mem})'

  def is_compatible_aval(self, aval_shape: Shape):
    num_ways_dim_sharded, _ = get_num_ways_dim_sharded(self._hlo_sharding)
    if len(aval_shape) < len(num_ways_dim_sharded):
      raise ValueError(
          f"Sharding {self} is only valid for values of rank at least "
          f"{len(num_ways_dim_sharded)}, but was applied to a value of rank "
          f"{len(aval_shape)}")

  @functools.cached_property
  def device_set(self) -> set[Device]:
    return set(self._devices)

  @property
  def memory_kind(self) -> str | None:
    return self._memory_kind

  def with_memory_kind(self, kind: str) -> GSPMDSharding:
    return GSPMDSharding(self._devices, self._hlo_sharding, memory_kind=kind)

  def devices_indices_map(self, global_shape: Shape) -> Mapping[Device, Index]:
    return gspmd_sharding_devices_indices_map(self, global_shape)

  @property
  def _device_assignment(self) -> XLADeviceAssignment:
    return self._devices

  def _to_xla_hlo_sharding(self, num_dimensions: int) -> xc.HloSharding:
    return self._hlo_sharding

  @functools.cached_property
  def is_fully_replicated(self) -> bool:
    return is_op_sharding_replicated(self._hlo_sharding)

  @functools.cached_property
  def is_fully_addressable(self) -> bool:
    return self._internal_device_list.is_fully_addressable  # type: ignore

  @classmethod
  def get_replicated(cls, device_assignment, *, memory_kind: str | None = None):
    return cls(tuple(device_assignment), get_replicated_hlo_sharding(),
               memory_kind=memory_kind)
