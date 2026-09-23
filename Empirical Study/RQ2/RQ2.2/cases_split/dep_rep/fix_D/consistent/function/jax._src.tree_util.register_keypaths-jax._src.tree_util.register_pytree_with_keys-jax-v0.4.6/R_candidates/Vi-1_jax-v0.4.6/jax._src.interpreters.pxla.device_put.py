def device_put(x, devices: Sequence[xb.xla_client.Device], replicate: bool=False) -> List[xb.xla_client.Buffer]:
  """Call device_put on a sequence of devices and return a flat sequence of buffers."""
  if replicate:
    return list(it.chain.from_iterable(dispatch.device_put(x, device) for device in devices))
  else:
    return list(it.chain.from_iterable(dispatch.device_put(val, device) for val, device in safe_zip(x, devices)))
