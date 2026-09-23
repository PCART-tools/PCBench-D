def assert_unreachable(x):
  raise AssertionError(f"Unhandled case: {type(x).__name__}")
