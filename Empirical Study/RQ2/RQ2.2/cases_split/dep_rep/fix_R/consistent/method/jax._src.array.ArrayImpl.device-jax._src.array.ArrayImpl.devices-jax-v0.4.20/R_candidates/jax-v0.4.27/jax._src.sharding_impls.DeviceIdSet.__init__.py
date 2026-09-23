  def __init__(self, name, *ids):
    self._name = name
    self._ids = frozenset(ids)
