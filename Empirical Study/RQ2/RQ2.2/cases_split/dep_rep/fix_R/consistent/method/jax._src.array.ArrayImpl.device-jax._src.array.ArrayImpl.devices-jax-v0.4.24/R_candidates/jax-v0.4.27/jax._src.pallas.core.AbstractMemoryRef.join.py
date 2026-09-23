  def join(self, other):
    assert isinstance(other, AbstractMemoryRef)
    return AbstractMemoryRef(self.inner_aval.join(other.inner_aval),
                             self.memory_space)
