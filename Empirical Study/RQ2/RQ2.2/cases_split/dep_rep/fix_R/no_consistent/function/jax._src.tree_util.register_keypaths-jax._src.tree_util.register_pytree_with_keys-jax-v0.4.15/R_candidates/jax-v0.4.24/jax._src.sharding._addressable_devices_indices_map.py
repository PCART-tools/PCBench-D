@functools.lru_cache(maxsize=4096)
def _addressable_devices_indices_map(
    sharding: Sharding, global_shape: Shape) -> Mapping[Device, Index | None]:
  global_map = sharding.devices_indices_map(global_shape)
  if sharding.is_fully_addressable:
    return global_map
  if hasattr(sharding, '_internal_device_list'):
    return {d: global_map[d]
            for d in sharding._internal_device_list.addressable_device_list}
  return {d: ind for d, ind in global_map.items()
          if d.process_index == d.client.process_index()}
