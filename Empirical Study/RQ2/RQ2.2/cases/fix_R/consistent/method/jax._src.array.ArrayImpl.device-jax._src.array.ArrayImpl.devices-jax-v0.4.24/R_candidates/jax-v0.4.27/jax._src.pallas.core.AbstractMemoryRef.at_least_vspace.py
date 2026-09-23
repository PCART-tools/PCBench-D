  def at_least_vspace(self):
    return AbstractMemoryRef(
        self.inner_aval.at_least_vspace(), self.memory_space)
