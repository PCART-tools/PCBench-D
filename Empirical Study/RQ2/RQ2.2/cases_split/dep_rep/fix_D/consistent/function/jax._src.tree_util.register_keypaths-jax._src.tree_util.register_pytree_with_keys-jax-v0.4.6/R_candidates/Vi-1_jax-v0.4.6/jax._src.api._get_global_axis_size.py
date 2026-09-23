def _get_global_axis_size(local_axis_size: int, in_devices, backend_name: str,
                          global_axis_size: Optional[int]):
  """Determine global_axis_size for multi-host pmap."""
  # TODO(mattjj,skyewm): revive this check (inner_pmap always False now)
  # if xb.process_count() > 1 and global_axis_size is None and inner_pmap:
  #   raise ValueError("'axis_size' must be specified for nested multi-host pmaps")
  if (xb.process_count() == 1 and global_axis_size is not None and
      global_axis_size != local_axis_size):
    raise ValueError(
        f"Specified axis_size {global_axis_size} doesn't match received "
        f"axis_size {local_axis_size}.")

  if in_devices is not None and backend_name is None:
    backend = xb.get_device_backend(in_devices[0])
  else:
    backend = xb.get_backend(backend_name)

  if global_axis_size is None:
    if xb.process_count(backend) == 1:
      global_axis_size = local_axis_size
    elif in_devices:
      global_axis_size = len(in_devices)
    else:
      global_axis_size = local_axis_size * xb.process_count(backend)
      assert all(
          len(xb.local_devices(pi, backend)) == xb.local_device_count(backend)
          for pi in range(xb.process_count(backend)))
  return global_axis_size
