  def replicate(self, axis=None, keepdims=True) -> PositionalSharding:
    new_ids = self._ids.sum(axis=axis, keepdims=keepdims)  # union
    return self._remake(self._devices, new_ids)
