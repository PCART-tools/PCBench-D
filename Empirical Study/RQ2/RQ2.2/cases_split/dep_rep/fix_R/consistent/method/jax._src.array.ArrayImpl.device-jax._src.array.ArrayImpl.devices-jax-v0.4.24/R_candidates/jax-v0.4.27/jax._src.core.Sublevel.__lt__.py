  def __lt__(self, other):
    return type(other) is Sublevel and self.level < other.level
