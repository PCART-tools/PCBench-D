def trace_function(*args, **kwargs):
  warnings.warn(
      "trace_function has been renamed to annotate_function. This alias "
      "will eventually be removed; please update your code.")
  return annotate_function(*args, **kwargs)
