def _copy_device_array_to_device(
    x: Union[device_array.DeviceArrayProtocol, device_array._DeviceArray],
    device: Optional[xc.Device]
  ) -> Union[device_array.DeviceArrayProtocol, device_array._DeviceArray]:
  if device is None:
    # no copying to be done because there's no target specified
    return x
  elif xb.get_device_backend(device).platform == x.device_buffer.platform():
    # source and target platforms are the same
    if x.device_buffer.device() == device:
      # no copying to be done because source equals target
      if x._device == device:
        return x
      else:
        moved_buf = x.device_buffer  # We need to change stickyness
    else:
      # move the buffer with a device-to-device copy
      moved_buf = x.device_buffer.copy_to_device(device)
  else:
    # buffers from different XLA backends are passed through the host.
    backend = xb.get_device_backend(device)
    moved_buf = backend.buffer_from_pyval(x.device_buffer.to_py(), device)
  return device_array.make_device_array(x.aval, device, moved_buf)
