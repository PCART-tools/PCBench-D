  def __hash__(self):
    return hash((self.f.__code__, self.closure))
