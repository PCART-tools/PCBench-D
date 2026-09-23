  def use_cpp_class(cpp_cls):
    """A helper decorator to replace a python class with its C++ version"""

    def wrapper(cls):
      if cpp_cls is None:
        return cls

      exclude_methods = {'__module__', '__dict__', '__doc__'}

      originals = {}
      for attr_name, attr in cls.__dict__.items():
        if attr_name not in exclude_methods:
          if hasattr(_original_func(attr), "_use_cpp"):
            originals[attr_name] = attr
          else:
            setattr(cpp_cls, attr_name, attr)

      cpp_cls.__doc__ = cls.__doc__
      # TODO(pschuh): Remove once fastpath is gone.
      cpp_cls._original_py_fns = originals
      return cpp_cls

    return wrapper
