  @classmethod
  def known(cls, const: core.Value) -> PartialVal:
    return PartialVal((None, const))
