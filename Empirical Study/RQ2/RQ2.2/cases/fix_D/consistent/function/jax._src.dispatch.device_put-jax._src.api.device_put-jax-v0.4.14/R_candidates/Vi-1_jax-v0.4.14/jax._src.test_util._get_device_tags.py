def _get_device_tags():
  """returns a set of tags defined for the device under test"""
  if is_device_rocm():
    device_tags = {device_under_test(), "rocm"}
  elif is_device_cuda():
    device_tags = {device_under_test(), "cuda"}
  else:
    device_tags = {device_under_test()}
  return device_tags
