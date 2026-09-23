def _normalize_to_sharding(device: xc.Device | Sharding | None) -> Sharding | None:
  if isinstance(device, xc.Device):
    return SingleDeviceSharding(device)
  else:
    return device
