class AbstractToken(AbstractValue):
  def join(self, other):
    if isinstance(other, AbstractToken):
      return self
    else:
      assert False, f"Cannot join {self} with {other}"
  def str_short(self, short_dtypes=False): return 'Tok'
  def at_least_vspace(self): return self
