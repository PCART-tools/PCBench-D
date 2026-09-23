def _shard_aval(size, axis: int, aval):
  try:
    return _shard_aval_handlers[type(aval)](size, axis, aval)
  except KeyError as err:
    raise TypeError(f"No _shard_aval handler for type: {type(aval)}") from err
