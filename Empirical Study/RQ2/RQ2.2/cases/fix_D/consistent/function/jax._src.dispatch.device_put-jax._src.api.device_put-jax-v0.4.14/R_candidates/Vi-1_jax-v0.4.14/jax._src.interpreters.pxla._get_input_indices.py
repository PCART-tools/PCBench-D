def _get_input_indices(
    avals: Sequence[ShapedArray],
    shardings: Sequence[sharding_impls.XLACompatibleSharding],
    da_object: _DeviceAssignment | Sequence[xc.Device],
) -> Sequence[tuple[Index | None, ...]]:

  input_indices = []
  if isinstance(da_object, _DeviceAssignment):
    num_addressable_devices = len(da_object.addressable_device_assignment)
  else:
    num_addressable_devices = len(
        [d for d in da_object if d.process_index == d.client.process_index()])

  for aval, sharding in zip(avals, shardings):
    if aval is core.abstract_token:
      index = _get_replicated_slices(num_addressable_devices, None)
    else:
      if sharding.is_fully_replicated:
        index = _get_replicated_slices(num_addressable_devices, aval.ndim)
      else:
        index = tuple(
            sharding.addressable_devices_indices_map(aval.shape).values())  # type: ignore
    input_indices.append(index)

  return input_indices
