  def __init__(self, path: str):
    """Sets up a cache at 'path'. Cached values may already be present."""
    self._path = pathlib.Path(path)
    self._path.mkdir(parents=True, exist_ok=True)
