def _device_put_token(_, device):
  backend = xb.get_device_backend(device)
  return (backend.buffer_from_pyval(np.zeros((), dtype=np.dtype(np.bool_)),
                                    device),)
