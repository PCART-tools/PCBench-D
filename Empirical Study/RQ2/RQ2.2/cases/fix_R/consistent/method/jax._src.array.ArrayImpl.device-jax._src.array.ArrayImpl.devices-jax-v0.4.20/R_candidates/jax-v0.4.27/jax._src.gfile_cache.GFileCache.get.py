  def get(self, key: str):
    """Returns None if 'key' isn't present."""
    if not key:
      raise ValueError("key cannot be empty")
    path_to_key = self._path / key
    if path_to_key.exists():
      return path_to_key.read_bytes()
    else:
      return None
