class DConcreteArray(DShapedArray):
  __slots__ = ['val']
  array_abstraction_level = 1
  def __init__(self, shape, dtype, weak_type, val):
    super().__init__(shape, dtype, weak_type)
    self.val = val
