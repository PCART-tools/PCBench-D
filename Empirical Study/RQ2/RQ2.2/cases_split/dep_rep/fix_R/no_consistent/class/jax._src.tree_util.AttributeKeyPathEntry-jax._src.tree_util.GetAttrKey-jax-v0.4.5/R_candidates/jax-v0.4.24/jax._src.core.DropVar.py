class DropVar(Var):
  def __init__(self, aval: AbstractValue):
    super().__init__(-1, '', aval)
  def __repr__(self): return '_'
