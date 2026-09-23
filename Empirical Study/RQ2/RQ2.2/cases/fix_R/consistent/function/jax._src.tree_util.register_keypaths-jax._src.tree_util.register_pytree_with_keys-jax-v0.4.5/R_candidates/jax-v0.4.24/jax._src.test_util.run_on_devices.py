def run_on_devices(*enabled_devices):
  """A decorator for test methods to run the test only on certain devices."""
  return _device_filter(lambda: test_device_matches(enabled_devices))
