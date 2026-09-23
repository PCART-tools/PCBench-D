@lru_cache(maxsize=2048)
def _create_da_object(  # pytype: disable=invalid-annotation
    device_assignment: tuple[xc.Device, ...]) -> _DeviceAssignment:  # type: ignore
  return _DeviceAssignment(device_assignment)
