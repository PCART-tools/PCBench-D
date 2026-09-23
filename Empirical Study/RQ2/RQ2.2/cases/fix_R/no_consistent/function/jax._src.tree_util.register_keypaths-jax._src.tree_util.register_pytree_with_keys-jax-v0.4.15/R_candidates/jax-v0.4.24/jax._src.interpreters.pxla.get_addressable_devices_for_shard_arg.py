@lru_cache(maxsize=1024)
def get_addressable_devices_for_shard_arg(
    s: sharding_impls.XLACompatibleSharding) -> tuple[xc.Device, ...]:
  return s._addressable_device_assignment
