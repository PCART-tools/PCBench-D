@total_ordering
class Var:
  __slots__ = ["count", "suffix", "aval"]

  count: int
  suffix: str
  aval: AbstractValue

  def __init__(self, count: int, suffix: str, aval: AbstractValue):
    self.count = count
    self.suffix = suffix
    self.aval = raise_to_shaped(aval)

  def __lt__(self, other):
    if not isinstance(other, Var):
      return NotImplemented
    else:
      return (self.count, self.suffix) < (other.count, other.suffix)

  def __repr__(self):
    return _encode_digits_alphabetic(self.count) + self.suffix
