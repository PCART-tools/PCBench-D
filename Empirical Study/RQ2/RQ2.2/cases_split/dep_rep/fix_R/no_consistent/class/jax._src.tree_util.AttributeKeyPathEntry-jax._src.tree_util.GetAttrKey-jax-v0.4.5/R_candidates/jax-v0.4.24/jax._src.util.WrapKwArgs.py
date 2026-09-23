class WrapKwArgs:
  __slots__ = ["val"]

  def __init__(self, val):
    self.val = val

  def __hash__(self):
    return hash(tuple((k, v) for k, v in sorted(self.val.items())))

  def __eq__(self, other):
    return self.val == other.val
