def _device_filter(predicate):
  def skip(test_method):
    @functools.wraps(test_method)
    def test_method_wrapper(self, *args, **kwargs):
      device_tags = _get_device_tags()
      if not predicate():
        test_name = getattr(test_method, '__name__', '[unknown test]')
        raise unittest.SkipTest(
          f"{test_name} not supported on device with tags {device_tags}.")
      return test_method(self, *args, **kwargs)
    return test_method_wrapper
  return skip
