  def __init__(self):
    self.canonicalize = functools.lru_cache(128)(lambda x: x)
