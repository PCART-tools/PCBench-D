def _get_and_check_device_assignment(
    shardings: Iterable[ShardingInfo],
    devices: Sequence[xc.Device] | None,
) -> tuple[xc.Client, tuple[xc.Device, ...]]:
  first_sharding_info = None
  if devices is None:
    devices = ()
  else:
    devices = tuple(devices)

  for i, s_type, source_info in shardings:
    if is_unspecified(i):
      continue

    if first_sharding_info is None:
      first_sharding_info = (
          (i.mesh._flat_devices_tuple, s_type, source_info) if is_auto(i)  # type: ignore
          else (i._device_assignment, s_type, source_info))  # type: ignore
    arr_device_assignment = i.mesh._flat_devices_tuple if is_auto(i) else i._device_assignment  # type: ignore
    if not devices:
      if first_sharding_info[0] != arr_device_assignment:
        raise DeviceAssignmentMismatchError([
            DeviceAssignmentMismatch(*first_sharding_info),
            DeviceAssignmentMismatch(arr_device_assignment, s_type, source_info)])
    else:
      if devices != arr_device_assignment:
        raise DeviceAssignmentMismatchError([
            DeviceAssignmentMismatch(devices, MismatchType.CONTEXT_DEVICES, None),
            DeviceAssignmentMismatch(arr_device_assignment, s_type, source_info)])
  if first_sharding_info is None and devices:
    final_device_assignment = devices
  elif first_sharding_info is None:
    final_device_assignment = (_get_default_device(),)
  else:
    final_device_assignment = first_sharding_info[0]
  return xb.get_device_backend(final_device_assignment[0]), final_device_assignment
