class Zero:
  __slots__ = ['aval']
  def __init__(self, aval: core.AbstractValue):
    self.aval = aval
  def __repr__(self) -> str:
    return f'Zero({self.aval})'
  @staticmethod
  def from_value(val: Any) -> Zero:
    return Zero(raise_to_shaped(get_aval(val)))
