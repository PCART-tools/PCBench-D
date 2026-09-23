  def join(self, other):
    assert isinstance(other, AbstractRef)
    return AbstractRef(self.inner_aval.join(other.inner_aval))
