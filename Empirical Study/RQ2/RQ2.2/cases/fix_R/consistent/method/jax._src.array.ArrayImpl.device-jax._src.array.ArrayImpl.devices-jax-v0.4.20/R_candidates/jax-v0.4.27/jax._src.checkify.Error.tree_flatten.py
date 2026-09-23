  def tree_flatten(self):
    return ((self._pred, self._code, self._payload), (self._metadata))
