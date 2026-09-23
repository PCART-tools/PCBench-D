def is_user_filename(filename: str) -> bool:
  """Heuristic that guesses the identity of the user's code in a stack trace."""
  return (filename.endswith("_test.py") or
          not any(filename.startswith(p) for p in _exclude_paths) or
          any(filename.startswith(p) for p in _include_paths))
