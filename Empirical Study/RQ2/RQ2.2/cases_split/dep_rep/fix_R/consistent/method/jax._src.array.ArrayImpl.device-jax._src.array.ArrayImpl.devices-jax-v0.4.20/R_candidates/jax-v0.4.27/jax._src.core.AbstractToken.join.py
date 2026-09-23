  def join(self, other):
    if isinstance(other, AbstractToken):
      return self
    else:
      assert False, f"Cannot join {self} with {other}"
