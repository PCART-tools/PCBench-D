  @classmethod
  def unknown(cls, aval: AbstractValue) -> PartialVal:
    return PartialVal((aval, None))
