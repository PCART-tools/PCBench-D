def _get_input_indices(
    avals: Sequence[ShapedArray],
    shardings: Sequence[sharding_impls.XLACompatibleSharding],
    da_object: _DeviceAssignment | Sequence[xc.Device],  # type: ignore
) -> Sequence[tuple[Index | None, ...]]:

  input_indices = []
  if not isinstance(da_object, _DeviceAssignment):
    da_object = _create_da_object(tuple(da_object))
  num_addressable_devices = len(da_object.addressable_device_list)

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
