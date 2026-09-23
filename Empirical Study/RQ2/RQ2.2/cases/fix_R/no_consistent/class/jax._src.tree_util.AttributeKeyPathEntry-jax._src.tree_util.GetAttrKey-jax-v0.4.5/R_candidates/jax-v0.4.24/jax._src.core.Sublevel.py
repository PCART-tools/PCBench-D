@total_ordering
class Sublevel:

  def __init__(self, level: int):
    self.level = level

  def __repr__(self):
    return str(self.level)

  def __eq__(self, other):
    return type(other) is Sublevel and self.level == other.level

  def __lt__(self, other):
    return type(other) is Sublevel and self.level < other.level
