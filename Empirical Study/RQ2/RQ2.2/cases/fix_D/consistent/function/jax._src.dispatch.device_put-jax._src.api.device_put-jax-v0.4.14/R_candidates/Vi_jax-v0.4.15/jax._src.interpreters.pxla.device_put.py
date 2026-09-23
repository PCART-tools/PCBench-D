def device_put(x, devices: Sequence[xc.ArrayImpl],
               replicate: bool=False) -> list[xc.ArrayImpl]:
  """Call device_put on a sequence of devices and return a flat sequence of buffers."""
  if replicate:
    return [jax.device_put(x, device) for device in devices]
  else:
    return [jax.device_put(val, device) for val, device in safe_zip(x, devices)]
