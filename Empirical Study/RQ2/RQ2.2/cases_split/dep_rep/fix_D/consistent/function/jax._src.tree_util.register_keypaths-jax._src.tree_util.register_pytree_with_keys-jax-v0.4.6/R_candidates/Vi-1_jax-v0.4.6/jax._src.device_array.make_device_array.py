def make_device_array(
    aval: core.ShapedArray,
    device: Optional[Device],
    device_buffer: Buffer,
) -> Union[Buffer, "_DeviceArray"]:
  """Returns a DeviceArray implementation based on arguments.

  This is to be used only within JAX. It will return either a PythonDeviceArray
  or a C++ equivalent implementation.
  """

  if isinstance(device_buffer, xc.Buffer):

    if device_buffer.aval == aval and device_buffer._device == device:
      return device_buffer
    device_buffer = device_buffer.clone()
    device_buffer._device = device
    device_buffer.aval = aval
    device_buffer.weak_type = aval.weak_type
    return device_buffer

  return _DeviceArray(aval, device, device_buffer)
