@functools.lru_cache(maxsize=4096)
def pmap_sharding_devices_indices_map(
    self, global_shape: Shape) -> Mapping[Device, Index]:
  self.shard_shape(global_shape)  # raises a good error message
  indices = sharding_specs.spec_to_indices(global_shape, self.sharding_spec)
  return dict(safe_zip(self.devices.flat, indices))  # type: ignore[arg-type]
