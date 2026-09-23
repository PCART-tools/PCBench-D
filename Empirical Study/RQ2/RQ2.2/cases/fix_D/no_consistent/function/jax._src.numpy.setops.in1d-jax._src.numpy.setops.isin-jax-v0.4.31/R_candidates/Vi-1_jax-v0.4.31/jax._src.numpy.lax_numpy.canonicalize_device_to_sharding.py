def canonicalize_device_to_sharding(device: xc.Device | Sharding | None
                                    ) -> Sharding | None:
  if isinstance(device, xc.Device):
    return SingleDeviceSharding(device)
  return device
