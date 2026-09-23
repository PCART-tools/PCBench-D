def _maybe_create_array_from_da(buf, aval, device):
  if config.jax_array:
    from jax.experimental.array import Array
    from jax.experimental.sharding import SingleDeviceSharding
    return Array(buf.shape, SingleDeviceSharding(buf.device()), [buf],
                 committed=(device is not None))
  else:
    return device_array.make_device_array(aval, device, buf)
