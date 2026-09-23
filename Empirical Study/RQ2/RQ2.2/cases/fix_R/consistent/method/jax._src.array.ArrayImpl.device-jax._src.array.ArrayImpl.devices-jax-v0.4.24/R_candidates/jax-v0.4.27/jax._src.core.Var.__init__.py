  def __init__(self, suffix: str, aval: AbstractValue):
    self.count = next(_var_counter)
    self.suffix = suffix
    self.aval = raise_to_shaped(aval)
