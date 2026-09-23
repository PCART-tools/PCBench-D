def _device_put_scalar(x, device):
  return _device_put_array(dtypes.coerce_to_array(x), device)
