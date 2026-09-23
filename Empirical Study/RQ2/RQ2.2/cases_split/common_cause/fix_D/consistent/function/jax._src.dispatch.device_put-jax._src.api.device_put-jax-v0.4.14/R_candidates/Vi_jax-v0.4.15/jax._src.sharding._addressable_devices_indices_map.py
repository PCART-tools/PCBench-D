@functools.lru_cache(maxsize=4096)
def _addressable_devices_indices_map(
    sharding: Sharding, global_shape: Shape) -> Mapping[Device, Index | None]:
  if sharding.is_fully_addressable:
    return sharding.devices_indices_map(global_shape)
  return {d: ind for d, ind in sharding.devices_indices_map(global_shape).items()
          if d.process_index == d.client.process_index()}
