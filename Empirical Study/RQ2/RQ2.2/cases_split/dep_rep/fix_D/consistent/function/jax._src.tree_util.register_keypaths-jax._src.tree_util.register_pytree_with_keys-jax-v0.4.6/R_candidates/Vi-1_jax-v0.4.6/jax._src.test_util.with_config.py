def with_config(**kwds):
  """Test case decorator for subclasses of JaxTestCase"""
  def decorator(cls):
    assert inspect.isclass(cls) and issubclass(cls, JaxTestCase), "@with_config can only wrap JaxTestCase class definitions."
    cls._default_config = {**JaxTestCase._default_config, **kwds}
    return cls
  return decorator
