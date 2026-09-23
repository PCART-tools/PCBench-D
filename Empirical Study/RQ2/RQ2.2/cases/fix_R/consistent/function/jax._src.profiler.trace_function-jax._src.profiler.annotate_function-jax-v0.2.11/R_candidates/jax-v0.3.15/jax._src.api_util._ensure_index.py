def _ensure_index(x: Any) -> Union[int, Tuple[int, ...]]:
  """Ensure x is either an index or a tuple of indices."""
  try:
    return operator.index(x)
  except TypeError:
    return tuple(map(operator.index, x))
