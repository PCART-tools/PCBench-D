  def reshape(self, *shape) -> PositionalSharding:
    return self._remake(self._devices, self._ids.reshape(*shape))
