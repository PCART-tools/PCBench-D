  def full_lower(self):
    if type(self.tangent) is Zero:
      return core.full_lower(self.primal)
    else:
      return self
