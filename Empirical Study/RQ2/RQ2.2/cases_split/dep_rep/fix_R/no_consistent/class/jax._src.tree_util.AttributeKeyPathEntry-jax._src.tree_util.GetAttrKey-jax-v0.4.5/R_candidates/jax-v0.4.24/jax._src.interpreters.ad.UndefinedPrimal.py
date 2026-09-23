class UndefinedPrimal:
  __slots__ = ['aval']
  def __init__(self, aval):
    self.aval = aval
  def __repr__(self):
    return f'UndefinedPrimal({self.aval})'
