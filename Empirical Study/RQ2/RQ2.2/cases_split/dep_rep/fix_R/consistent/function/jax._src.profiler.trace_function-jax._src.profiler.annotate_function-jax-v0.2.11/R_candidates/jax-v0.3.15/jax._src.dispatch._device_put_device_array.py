def _device_put_device_array(x: Union[device_array.DeviceArrayProtocol, device_array._DeviceArray], device: Optional[Device]):
  x = _copy_device_array_to_device(x, device)
  return (x.device_buffer,)
