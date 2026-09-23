@functools.lru_cache(maxsize=4096)
def common_devices_indices_map(s, global_shape: Shape) -> Mapping[Device, Index]:
  hlo_sharding = s._to_xla_hlo_sharding(len(global_shape))
  gspmd_sharding = GSPMDSharding(s._device_assignment, hlo_sharding)
  return gspmd_sharding.devices_indices_map(global_shape)
