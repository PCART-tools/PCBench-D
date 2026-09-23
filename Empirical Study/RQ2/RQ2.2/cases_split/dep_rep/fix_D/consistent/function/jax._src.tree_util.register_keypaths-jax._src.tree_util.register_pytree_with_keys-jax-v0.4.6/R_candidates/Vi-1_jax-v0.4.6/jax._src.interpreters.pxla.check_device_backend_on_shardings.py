def check_device_backend_on_shardings(shardings) -> bool:
  for i in shardings:
    if _is_unspecified(i) or is_auto(i):
      continue
    if hasattr(i, '_original_sharding') and getattr(
        i._original_sharding, '_device_backend', False):
      return True
  return False
