def use_cpp_class(cpp_cls):
  """A helper decorator to replace a python class with its C++ version"""

  def wrapper(cls):
    if TYPE_CHECKING or cpp_cls is None:
      return cls

    exclude_methods = {'__module__', '__dict__', '__doc__'}

    for attr_name, attr in cls.__dict__.items():
      if attr_name not in exclude_methods and not hasattr(
          _original_func(attr), "_use_cpp"):
        setattr(cpp_cls, attr_name, attr)

    cpp_cls.__doc__ = cls.__doc__

    return cpp_cls

  return wrapper
