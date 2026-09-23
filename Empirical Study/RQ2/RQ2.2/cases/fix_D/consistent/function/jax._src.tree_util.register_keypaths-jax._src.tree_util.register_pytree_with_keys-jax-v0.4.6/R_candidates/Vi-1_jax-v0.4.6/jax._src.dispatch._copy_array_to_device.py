def _copy_array_to_device(x: jax.Array, device: Optional[xc.Device]) -> jax.Array:
  """Copies `Array`s with SingleDeviceSharding to a different device."""
  if device is None:
    # no copying to be done because there's no target specified
    return x

  buf = x._arrays[0]
  if xb.get_device_backend(device).platform == buf.platform():
    # source and target platforms are the same
    if x.device() == device:
      # no copying to be done because source equals target
      if x._committed:
        return x
      else:
        moved_buf = buf  # We need to change stickyness
    else:
      # move the buffer with a device-to-device copy
      moved_buf = buf.copy_to_device(device)
  else:
    # buffers from different XLA backends are passed through the host.
    backend = xb.get_device_backend(device)
    moved_buf = backend.buffer_from_pyval(np.asarray(buf), device)
  return array.ArrayImpl(
      x.aval, SingleDeviceSharding(moved_buf.device()), [moved_buf],
      committed=(device is not None))
