class Shard:
  """A single data shard of an Array.

  Attributes:
    device : Which device this shard resides on.
    index : The index into the global array of this shard.
    replica_id : Integer id indicating which replica of the global array this
      shard is part of. Always 0 for fully sharded data
      (i.e. when there’s only 1 replica).
    data : The data of this shard. None if ``device`` is non-local.
  """

  def __init__(self, device: Device, sharding: Sharding, global_shape: Shape,
               data: None | ArrayImpl | PRNGKeyArray = None):
    self._device = device
    self._sharding = sharding
    self._global_shape = global_shape
    self._data = data

  def __repr__(self):
    try:
      return (f'Shard(device={self.device!r}, index={self.index}, '
              f'replica_id={self.replica_id}, data={self.data})')
    except ValueError:
      return f'Shard(device={self.device!r}, data={self.data})'

  @functools.cached_property
  def index(self) -> Index:
    try:
      device_indices_map_fn = self._sharding.devices_indices_map
    except AttributeError:
      raise ValueError('Cannot calculate indices from sharding: '
                       f'{self._sharding}. Please create a device to index '
                       'mapping for your sharding.') from None
    index = device_indices_map_fn(self._global_shape)[self.device]
    assert index is not None
    return index

  @functools.cached_property
  def replica_id(self) -> int:
    return device_replica_id_map(self._sharding, self._global_shape)[self.device]

  @property
  def device(self):
    return self._device

  @property
  def data(self):
    return self._data
