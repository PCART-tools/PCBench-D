def with_config(**kwds):
  """Test case decorator for subclasses of JaxTestCase"""
  def decorator(cls):
    assert inspect.isclass(cls) and issubclass(cls, JaxTestCase), "@with_config can only wrap JaxTestCase class definitions."
    cls._default_config = {}
    for b in cls.__bases__:
      cls._default_config.update(b._default_config)
    cls._default_config.update(kwds)
    return cls
  return decorator
