def shard_aval(size, axis: int, aval):
  try:
    return shard_aval_handlers[type(aval)](size, axis, aval)
  except KeyError as err:
    raise TypeError(f"No shard_aval handler for type: {type(aval)}") from err
