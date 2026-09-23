def _extract_function_name(f: Callable, name: str | None) -> str:
  if name is None:
    name = f.__name__ if hasattr(f, "__name__") and f.__name__ else "func"
  return name
