def default_backend() -> str:
  """Returns the platform name of the default XLA backend."""
  return get_backend(None).platform
