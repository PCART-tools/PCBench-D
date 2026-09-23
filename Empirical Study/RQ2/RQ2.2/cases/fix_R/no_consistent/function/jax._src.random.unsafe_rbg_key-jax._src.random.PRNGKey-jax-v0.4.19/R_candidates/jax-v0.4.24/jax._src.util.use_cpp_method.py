  def use_cpp_method(is_enabled=True):
    """A helper decorator to exclude methods from the set that are forwarded to C++ class"""
    def decorator(f):
      if is_enabled:
        original_func = _original_func(f)
        original_func._use_cpp = True
      return f

    if not isinstance(is_enabled, bool):
      raise TypeError(
          "Decorator got wrong type: @use_cpp_method(is_enabled: bool=True)"
      )
    return decorator
