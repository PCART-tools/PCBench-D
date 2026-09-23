class PositionalSharding(XLACompatibleSharding):
  _devices: tuple[xc.Device, ...]
  _memory_kind: str | None
  _ids: np.ndarray  # dtype DeviceIdSet

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

  @property
  def shape(self):
    return self._ids.shape

  @property
  def ndim(self):
    return self._ids.ndim

  def __repr__(self) -> str:
    cls_name = self.__class__.__name__
    ids = self._ids.copy()
    platform_name = self._devices[0].platform.upper()
    for idx, x in np.ndenumerate(ids):
      ids[idx] = DeviceIdSet(platform_name, *(self._devices[i].id for i in x))
    body = np.array2string(ids, prefix=cls_name + '(', suffix=')',
                           max_line_width=100)
    mem = '' if self._memory_kind is None else f', memory_kind={self._memory_kind}'
    return f'{cls_name}({body}{mem}, shape={self.shape})'

  def reshape(self, *shape) -> PositionalSharding:
    return self._remake(self._devices, self._ids.reshape(*shape))

  def transpose(self, *axes) -> PositionalSharding:
    return self._remake(self._devices, self._ids.transpose(*axes))
  T = property(transpose)

  def replicate(self, axis=None, keepdims=True) -> PositionalSharding:
    new_ids = self._ids.sum(axis=axis, keepdims=keepdims)  # union
    return self._remake(self._devices, new_ids)

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

  # Hashable

  def __hash__(self) -> int:
    if not hasattr(self, '_hash'):
      self._hash = hash((self._internal_device_list, self.memory_kind))
    return self._hash

  def __eq__(self, other) -> bool:
    if not isinstance(other, PositionalSharding):
      return False
    if id(self) == id(other):
      return True
    all_ids_equal = np.array_equal(self._ids,other._ids)
    mem_kind_equal = self.memory_kind == other.memory_kind
    if (id(self._devices) == id(other._devices) and mem_kind_equal and
        all_ids_equal):
      return True
    return (mem_kind_equal and all_ids_equal and
            self._internal_device_list == other._internal_device_list)

  # Sharding interface

  @functools.cached_property
  def device_set(self) -> set[xc.Device]:
    return set(self._devices)

  @property
  def memory_kind(self) -> str | None:
    return self._memory_kind

  def with_memory_kind(self, kind: str) -> PositionalSharding:
    return PositionalSharding(self._devices, memory_kind=kind)

  @functools.cached_property
  def is_fully_replicated(self) -> bool:
    return self.shape == (1,) * self.ndim

  # XLACompatibleSharding interface

  @property
  def _device_assignment(self) -> XLADeviceAssignment:
    return self._devices

  def _to_xla_hlo_sharding(self, num_dimensions: int) -> xc.HloSharding:
    return _positional_sharding_to_xla_hlo_sharding(self, num_dimensions)

  @functools.cached_property
  def is_fully_addressable(self) -> bool:
    return self._internal_device_list.is_fully_addressable
