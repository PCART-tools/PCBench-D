def is_special_dim_size(v: Any) -> bool:
  """Checks if a value is a special DimSize."""
  handler = _get_special_dim_handler(v)
  return (handler is not None)
