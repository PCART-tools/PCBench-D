@lru_cache(maxsize=1024)
def _get_replicated_slices(num_addressable_devices: int):
  return ((slice(None),),) * num_addressable_devices
