@lru_cache(maxsize=2048)
def _create_da_object(  # pytype: disable=invalid-annotation
    device_assignment: tuple[xc.Device, ...]) -> xc.DeviceList:  # type: ignore
  return xc.DeviceList(device_assignment)
