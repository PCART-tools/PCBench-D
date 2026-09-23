  def __hash__(self) -> int:
    return hash((self.level, self.trace_type))
