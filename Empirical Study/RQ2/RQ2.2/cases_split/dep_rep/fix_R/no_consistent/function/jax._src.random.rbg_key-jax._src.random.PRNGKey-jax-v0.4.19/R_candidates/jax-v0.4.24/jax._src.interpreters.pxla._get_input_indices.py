  def _get_input_indices(
      avals: Sequence[ShapedArray],
      shardings: Sequence[sharding_impls.XLACompatibleSharding],
      da_object: xc.DeviceList | Sequence[xc.Device],  # type: ignore
  ) -> Sequence[tuple[Index | None, ...]]:

    input_indices = []
    if not isinstance(da_object, xc.DeviceList):
      da_object = _create_da_object(tuple(da_object))
    num_addressable_devices = len(da_object.addressable_device_list)

    def _get_replicated_slices(num_addressable_devices: int, ndim: int | None):
      if ndim is None:
        return ((slice(None),),) * num_addressable_devices
      else:
        return ((slice(None),) * ndim,) * num_addressable_devices

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
