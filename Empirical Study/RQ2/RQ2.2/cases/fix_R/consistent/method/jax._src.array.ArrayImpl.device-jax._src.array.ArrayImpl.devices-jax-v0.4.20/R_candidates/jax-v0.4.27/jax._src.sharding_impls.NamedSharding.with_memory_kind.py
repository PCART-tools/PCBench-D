  def with_memory_kind(self, kind: str) -> NamedSharding:
    return NamedSharding(self.mesh, self.spec, memory_kind=kind)
