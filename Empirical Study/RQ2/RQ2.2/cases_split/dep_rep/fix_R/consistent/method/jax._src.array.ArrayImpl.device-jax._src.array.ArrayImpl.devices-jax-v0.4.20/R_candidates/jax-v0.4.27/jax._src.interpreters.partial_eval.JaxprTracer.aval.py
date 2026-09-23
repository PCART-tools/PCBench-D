  @property
  def aval(self) -> AbstractValue:
    return self.pval.get_aval()
