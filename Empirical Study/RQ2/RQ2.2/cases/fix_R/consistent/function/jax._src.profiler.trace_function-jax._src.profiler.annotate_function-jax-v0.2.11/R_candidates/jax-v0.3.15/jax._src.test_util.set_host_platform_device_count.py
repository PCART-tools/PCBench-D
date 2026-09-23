def set_host_platform_device_count(nr_devices: int):
  """Returns a closure that undoes the operation."""
  prev_xla_flags = os.getenv("XLA_FLAGS")
  flags_str = prev_xla_flags or ""
  # Don't override user-specified device count, or other XLA flags.
  if "xla_force_host_platform_device_count" not in flags_str:
    os.environ["XLA_FLAGS"] = (flags_str +
                               f" --xla_force_host_platform_device_count={nr_devices}")
  # Clear any cached backends so new CPU backend will pick up the env var.
  xla_bridge.get_backend.cache_clear()
  def undo():
    if prev_xla_flags is None:
      del os.environ["XLA_FLAGS"]
    else:
      os.environ["XLA_FLAGS"] = prev_xla_flags
    xla_bridge.get_backend.cache_clear()
  return undo
