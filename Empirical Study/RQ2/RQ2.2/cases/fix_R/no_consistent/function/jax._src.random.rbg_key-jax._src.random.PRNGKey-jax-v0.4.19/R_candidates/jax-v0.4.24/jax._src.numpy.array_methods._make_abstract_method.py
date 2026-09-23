def _make_abstract_method(name, func):
  @abc.abstractmethod
  @wraps(func)
  def method(*args, **kwargs):
    raise NotImplementedError(f"Cannot call abstract method {name}")
  return method
