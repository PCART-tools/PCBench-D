def pytest_mark_if_available(marker: str):
  """A decorator for test classes or methods to pytest.mark if installed."""
  def wrap(func_or_class):
    try:
      import pytest
    except ImportError:
      return func_or_class
    return getattr(pytest.mark, marker)(func_or_class)
  return wrap
