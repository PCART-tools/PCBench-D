class Literal:
  __slots__ = ["val", "aval", "hash"]

  val: Any
  aval: AbstractValue
  hash: int | None

  def __init__(self, val, aval):
    self.val = val
    self.aval = aval
    try:
      self.hash = hash(val)
    except TypeError:
      if type(val) in literalable_types:
        try:
          self.hash = hash((val.item(), val.dtype))
        except (TypeError, AttributeError, ValueError):
          self.hash = None

  __hash__ = None  # type: ignore

  def __repr__(self):
    if hasattr(self, 'hash'):
      return f'{self.val}'
    else:
      return f'Literal(val={self.val})'
