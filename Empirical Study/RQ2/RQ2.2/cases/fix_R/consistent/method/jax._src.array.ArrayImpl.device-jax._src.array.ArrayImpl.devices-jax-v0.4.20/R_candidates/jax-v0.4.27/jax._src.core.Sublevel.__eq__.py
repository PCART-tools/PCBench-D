  def __eq__(self, other):
    return type(other) is Sublevel and self.level == other.level
