def skip_on_devices(*disabled_devices):
  """A decorator for test methods to skip the test on certain devices."""
  return _device_filter(lambda: not test_device_matches(disabled_devices))
