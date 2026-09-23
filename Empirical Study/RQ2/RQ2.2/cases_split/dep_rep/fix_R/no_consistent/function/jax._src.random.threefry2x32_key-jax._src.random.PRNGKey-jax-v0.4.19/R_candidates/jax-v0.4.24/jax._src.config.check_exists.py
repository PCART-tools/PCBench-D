def check_exists(name):
  if name not in config.values:
    raise AttributeError(f"Unrecognized config option: {name}")
