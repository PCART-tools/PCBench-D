def _get_and_check_device_assignment(
    shardings: Iterable[ShardingInfo],
    devices: Optional[Sequence[xc.Device]],
) -> Tuple[xc.Client, Sequence[xc.Device]]:
  first_sharding_info = None
  if devices is None:
    devices = []
  else:
    devices = list(devices)

  for i, s_type, source_info in shardings:
    if is_auto(i) or _is_unspecified(i):
      continue
    # Assign `first_sharding_info` after `AUTO` and `UNSPECIFIED` have been
    # skipped.
    if first_sharding_info is None:
      first_sharding_info = (list(i._device_assignment), s_type, source_info)  # type: ignore
    arr_device_assignment = list(i._device_assignment)  # type: ignore
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
    final_device_assignment = [config.jax_default_device or xb.local_devices()[0]]
  else:
    final_device_assignment = first_sharding_info[0]
  return xb.get_device_backend(final_device_assignment[0]), final_device_assignment
