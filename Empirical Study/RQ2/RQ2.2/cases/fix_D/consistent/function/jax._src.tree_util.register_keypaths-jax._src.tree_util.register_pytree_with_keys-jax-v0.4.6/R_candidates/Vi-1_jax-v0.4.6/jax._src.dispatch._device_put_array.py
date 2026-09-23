def _device_put_array(x, device: Optional[Device]):
  backend = xb.get_device_backend(device)
  if x.dtype == dtypes.float0:
    x = np.zeros(x.shape, dtype=np.dtype(bool))
  return (backend.buffer_from_pyval(x, device),)
