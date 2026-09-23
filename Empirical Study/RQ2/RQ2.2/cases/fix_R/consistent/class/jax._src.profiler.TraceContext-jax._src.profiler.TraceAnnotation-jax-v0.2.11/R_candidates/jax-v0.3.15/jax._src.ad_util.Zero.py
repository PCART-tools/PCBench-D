class Zero:
  __slots__ = ['aval']
  def __init__(self, aval):
    self.aval = aval
  def __repr__(self):
    return f'Zero({self.aval})'
  @staticmethod
  def from_value(val):
    return Zero(raise_to_shaped(get_aval(val)))
