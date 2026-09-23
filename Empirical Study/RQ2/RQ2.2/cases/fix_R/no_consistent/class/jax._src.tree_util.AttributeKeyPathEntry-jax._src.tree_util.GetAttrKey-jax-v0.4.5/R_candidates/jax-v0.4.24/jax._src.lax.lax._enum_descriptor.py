class _enum_descriptor:
  def __init__(self, val):
    self.val = val
  def __get__(self, _, owner):
    return owner(self.val)
