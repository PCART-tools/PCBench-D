  def with_memory_kind(self, kind: str) -> PositionalSharding:
    return PositionalSharding(self._devices, memory_kind=kind)
