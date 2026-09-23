def tpu_enhanced_barrier_supported() -> bool:
  """Returns if tpu_enhanced_barrier flag is supported on this TPU version."""
  _, device_id = num_available_tpu_chips_and_device_id()
  return device_id in _TPU_ENHANCED_BARRIER_SUPPORTED
