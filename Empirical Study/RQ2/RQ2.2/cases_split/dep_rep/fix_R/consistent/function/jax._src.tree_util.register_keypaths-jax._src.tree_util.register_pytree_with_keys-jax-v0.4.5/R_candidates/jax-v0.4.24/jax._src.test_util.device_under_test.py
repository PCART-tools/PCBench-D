def device_under_test():
  return _TEST_DUT.value or xla_bridge.get_backend().platform
