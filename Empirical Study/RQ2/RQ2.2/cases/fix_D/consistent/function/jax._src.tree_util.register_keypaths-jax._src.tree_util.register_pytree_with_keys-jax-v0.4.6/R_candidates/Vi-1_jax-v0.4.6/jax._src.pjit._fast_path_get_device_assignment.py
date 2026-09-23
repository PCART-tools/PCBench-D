def _fast_path_get_device_assignment(
    shardings: Iterable[PjitSharding]) -> Optional[XLADeviceAssignment]:
  da = None
  for i in shardings:
    if is_auto(i) or _is_unspecified(i):
      continue
    da = i._device_assignment  # type: ignore
    break
  return da
