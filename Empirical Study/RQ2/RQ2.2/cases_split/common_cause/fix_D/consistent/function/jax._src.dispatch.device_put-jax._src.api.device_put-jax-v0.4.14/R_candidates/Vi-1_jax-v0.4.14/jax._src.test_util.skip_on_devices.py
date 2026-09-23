def skip_on_devices(*disabled_devices):
  """A decorator for test methods to skip the test on certain devices."""
  def skip(test_method):
    @functools.wraps(test_method)
    def test_method_wrapper(self, *args, **kwargs):
      device_tags = _get_device_tags()
      if device_tags & set(disabled_devices):
        test_name = getattr(test_method, '__name__', '[unknown test]')
        raise unittest.SkipTest(
          f"{test_name} not supported on device with tags {device_tags}.")
      return test_method(self, *args, **kwargs)
    return test_method_wrapper
  return skip
