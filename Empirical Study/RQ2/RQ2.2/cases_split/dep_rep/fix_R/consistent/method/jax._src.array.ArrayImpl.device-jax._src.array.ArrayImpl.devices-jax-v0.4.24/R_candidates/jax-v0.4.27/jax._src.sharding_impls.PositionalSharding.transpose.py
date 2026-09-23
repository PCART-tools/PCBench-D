  def transpose(self, *axes) -> PositionalSharding:
    return self._remake(self._devices, self._ids.transpose(*axes))
