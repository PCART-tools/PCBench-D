def _ensure_str(x: str) -> str:
  if not isinstance(x, str):
    raise TypeError(f"argument is not a string: {x}")
  return x
