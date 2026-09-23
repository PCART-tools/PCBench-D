class CacheInterface(util.StrictABC):
  _path: pathlib.Path

  @abstractmethod
  def get(self, key: str):
    pass

  @abstractmethod
  def put(self, key: str, value: bytes):
    pass
