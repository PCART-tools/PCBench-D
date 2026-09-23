  def __eq__(self, other: object) -> bool:
    return (isinstance(other, MainTrace) and
            self.level == other.level and
            self.trace_type == other.trace_type and
            self.payload == other.payload)
