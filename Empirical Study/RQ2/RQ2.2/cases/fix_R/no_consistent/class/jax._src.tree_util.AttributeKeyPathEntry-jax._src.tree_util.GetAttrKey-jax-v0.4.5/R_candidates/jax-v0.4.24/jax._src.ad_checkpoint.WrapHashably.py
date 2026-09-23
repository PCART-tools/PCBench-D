class WrapHashably:
  val: Any
  hash: int
  hashable: bool

  def __init__(self, val):
    self.val = val
    try:
      self.hash = hash(val)
      self.hashable = True
    except:
      self.hash = id(val)
      self.hashable = False
  def __hash__(self):
    return self.hash
  def __eq__(self, other):
    if isinstance(other, WrapHashably):
      if self.hashable and other.hashable:
        return self.val == other.val
      else:
        return self.val is other.val
    return False
