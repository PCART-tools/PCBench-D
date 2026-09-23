@use_cpp_class(xc.PmapSharding)
class PmapSharding(XLACompatibleSharding):
  """Describes a sharding used by :func:`jax.pmap`."""
  devices: np.ndarray
  sharding_spec: sharding_specs.ShardingSpec

  @use_cpp_method()
  def __init__(self, devices: Sequence[Device] | np.ndarray,
               sharding_spec: sharding_specs.ShardingSpec):
    self.devices = np.asarray(devices)
    # The sharding spec should be pmap's sharding spec.
    self.sharding_spec = sharding_spec

  def __reduce__(self):
    return (type(self), (self.devices, self.sharding_spec),
            {'memory_kind': self.memory_kind})

  def __eq__(self, other):
    if not isinstance(other, PmapSharding):
      return False
    if id(self) == id(other):
      return True
    return (self.sharding_spec == other.sharding_spec and
            self.devices.shape == other.devices.shape and
            self._internal_device_list == other._internal_device_list)  # type: ignore

  def __hash__(self):
    if not hasattr(self, '_hash'):
      self._hash = hash((self._internal_device_list, self.sharding_spec))  # type: ignore
    return self._hash

  def __str__(self):
    device_ids = [d.id for d in self.devices.flat]
    return (f'PmapSharding(sharding_spec={self.sharding_spec}, '
            f'{device_ids=}, '
            f'device_platform={self.devices.flat[0].platform.upper()}, '
            f'device_shape={self.devices.shape})')

  def __repr__(self):
    return (f'PmapSharding(sharding_spec={self.sharding_spec}, '
            f'devices={self.devices})')

  def is_equivalent_to(self: PmapSharding, other: PmapSharding,  # type: ignore
                       ndim: int) -> bool:
    return self == other

  # TODO(yashkatariya): Expose `sharded_dim_size` in the API if required.
  @classmethod
  def default(cls, shape: Shape, sharded_dim: int = 0,
              devices: Sequence[xc.Device] | None = None) -> PmapSharding:
    """Creates a :class:`PmapSharding` which matches the default placement
    used by :func:`jax.pmap`.

    Args:
      shape: The shape of the input array.
      sharded_dim: Dimension the input array is sharded on. Defaults to 0.
      devices: Optional sequence of devices to use. If omitted, the implicit
      device order used by pmap is used, which is the order of
        :func:`jax.local_devices`.
    """
    # The dtype doesn't matter here. Its only used for creating the
    # sharding_spec.
    sharding_spec = sharding_specs.create_pmap_sharding_spec(
        tuple(shape), sharded_dim)

    num_ways_sharded = None
    for s in sharding_spec.sharding:
      if isinstance(s, sharding_specs.Unstacked):
        assert num_ways_sharded is None
        num_ways_sharded = s.size
      elif isinstance(s, sharding_specs.Chunked):
        assert num_ways_sharded is None
        if len(s.chunks) == 1:
          num_ways_sharded = s.chunks[0]
        else:
          raise NotImplementedError(
              'Multiple chunks in Chunked dimension not supported.')

    if num_ways_sharded is None:
      raise NotImplementedError(
          '`None` to sharded_dim is not supported. Please file a jax '
          'issue if you need this feature.')

    if devices is None:
      pmap_devices: np.ndarray = np.array(
          xla_bridge.local_devices()[:num_ways_sharded])
    else:
      pmap_devices = np.array(devices)
    return cls(pmap_devices, sharding_spec)

  @functools.cached_property
  def device_set(self) -> set[Device]:
    return set(self.devices.flat)

  def devices_indices_map(self, global_shape: Shape) -> Mapping[Device, Index]:
    return pmap_sharding_devices_indices_map(self, global_shape)

  @functools.cached_property
  def _device_assignment(self) -> XLADeviceAssignment:
    return tuple(self.devices.flat)

  @property
  def memory_kind(self) -> str | None:
    try:
      return self._internal_device_list.default_memory_kind  # type: ignore
    except:
      return None

  def with_memory_kind(self, kind: str):
    raise NotImplementedError("pmap does not support memories.")

  def _to_xla_hlo_sharding(self, num_dimensions: int) -> xc.HloSharding:
    raise NotImplementedError("pmap doesn't use OpSharding.")

  @functools.cached_property
  def is_fully_replicated(self) -> bool:
    for s in self.sharding_spec.sharding:
      if isinstance(s, (sharding_specs.Unstacked, sharding_specs.Chunked)):
        return False
    return True

  @functools.cached_property
  def is_fully_addressable(self) -> bool:
    return self._internal_device_list.is_fully_addressable  # type: ignore

  def shard_shape(self, global_shape: Shape) -> Shape:
    sharded_dim = None
    sharded_dim_size = None
    for i, s in enumerate(self.sharding_spec.sharding):
      if isinstance(s, sharding_specs.Unstacked):
        sharded_dim = i
        sharded_dim_size = s.size
        sharded_shape = util.tuple_delete(global_shape, sharded_dim)
        break
      elif isinstance(s, sharding_specs.Chunked):
        sharded_dim = i
        assert len(s.chunks) == 1, s.chunks
        sharded_dim_size = s.chunks[0]
        sharded_shape = util.tuple_update(global_shape, sharded_dim, 1)
        break
    if sharded_dim is None:
      return global_shape
    if global_shape[sharded_dim] != sharded_dim_size:
      raise ValueError(
          f'The sharded dimension must be equal to the number of '
          f'devices passed to PmapSharding. Got sharded dimension {sharded_dim} '
          f'with value {global_shape[sharded_dim]} in shape {global_shape} and '
          f'the number of devices={len(self._device_assignment)}')
    return sharded_shape
