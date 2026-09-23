@lru_cache(maxsize=2048)
def _create_da_object(
    device_assignment: tuple[xc.Device, ...]) -> _DeviceAssignment:
  return _DeviceAssignment(device_assignment)
