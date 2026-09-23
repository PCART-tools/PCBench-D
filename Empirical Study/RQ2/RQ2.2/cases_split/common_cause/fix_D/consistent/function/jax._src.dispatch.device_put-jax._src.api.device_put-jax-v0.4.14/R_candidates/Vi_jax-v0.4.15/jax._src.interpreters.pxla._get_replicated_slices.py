@lru_cache(maxsize=1024)
def _get_replicated_slices(num_addressable_devices: int, ndim: int | None):
  if ndim is None:
    return ((slice(None),),) * num_addressable_devices
  else:
    return ((slice(None),) * ndim,) * num_addressable_devices
