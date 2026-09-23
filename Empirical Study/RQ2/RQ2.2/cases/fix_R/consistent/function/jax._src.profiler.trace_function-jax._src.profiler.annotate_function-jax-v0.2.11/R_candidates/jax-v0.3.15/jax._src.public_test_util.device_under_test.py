def device_under_test():
  return getattr(FLAGS, 'jax_test_dut', None) or xla_bridge.get_backend().platform
