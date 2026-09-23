def _gspmd_to_single_device_sharding(
    out_s: GSPMDSharding, orig_in_s: SingleDeviceSharding) -> SingleDeviceSharding:
  assert isinstance(orig_in_s, SingleDeviceSharding)
  return SingleDeviceSharding(
      out_s._device_assignment[0], memory_kind=out_s.memory_kind)
