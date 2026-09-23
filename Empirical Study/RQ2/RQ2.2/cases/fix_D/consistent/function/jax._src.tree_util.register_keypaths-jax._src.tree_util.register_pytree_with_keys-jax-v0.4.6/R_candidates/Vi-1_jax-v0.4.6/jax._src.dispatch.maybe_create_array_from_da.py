def maybe_create_array_from_da(buf, aval, device):
  if config.jax_array:
    return array.ArrayImpl(aval, SingleDeviceSharding(buf.device()), [buf],
                           committed=(device is not None), _skip_checks=True)
  else:
    return device_array.make_device_array(aval, device, buf)
