def _fast_path_get_device_assignment(
    shardings: Iterable[PjitSharding]) -> Optional[XLADeviceAssignment]:
  da = None
  for i in shardings:
    if is_unspecified(i):
      continue
    if is_auto(i):
      return i.mesh._flat_devices_tuple  # type: ignore
    return i._device_assignment  # type: ignore
  return da
