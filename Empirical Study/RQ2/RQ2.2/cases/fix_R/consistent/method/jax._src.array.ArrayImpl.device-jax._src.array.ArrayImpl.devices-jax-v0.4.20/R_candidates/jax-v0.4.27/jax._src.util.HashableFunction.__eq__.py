  def __eq__(self, other):
    return (type(other) is HashableFunction and
            self.f.__code__ == other.f.__code__ and
            self.closure == other.closure)
